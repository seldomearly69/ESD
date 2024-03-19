from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import pika
import time, sys

app = Flask(__name__)
CORS(app)

hostname = "rabbitmq" # default hostname
port = 5672            # default port
user="username"
password="password"
exchangename = "email_exchange" 
exchangetype = "topic"

def create_connection(max_retries=12, retry_interval=5):
    print('amqp_connection: Create_connection')
    
    retries = 0
    connection = None
    
    # loop to retry connection upto 12 times with a retry interval of 5 seconds
    while retries < max_retries:
        try:
            print('amqp_connection: Trying connection')
            # connect to the broker
            credentials=pika.PlainCredentials(user,password)
            connection = pika.BlockingConnection(pika.ConnectionParameters
                                (host=hostname, port=port,
                                 heartbeat=3600, blocked_connection_timeout=3600,credentials=credentials)) # these parameters to prolong the expiration time (in seconds) of the connection
                # Note about AMQP connection: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
                # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls.
                # If see: Stream connection lost: ConnectionResetError(10054, 'An existing connection was forcibly closed by the remote host', None, 10054, None)
                # - Try: simply re-run the program or refresh the page.
                # For rare cases, it's incompatibility between RabbitMQ and the machine running it,
                # - Use the Docker version of RabbitMQ instead: https://www.rabbitmq.com/download.html
            print("amqp_connection: Connection established successfully")
            break  # Connection successful, exit the loop
        except pika.exceptions.AMQPConnectionError as e:
            print(f"amqp_connection: Failed to connect: {e}")
            retries += 1
            print(f"amqp_connection: Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
    
    if connection is None:
        raise Exception("Unable to establish a connection to RabbitMQ after multiple attempts")
    
    return connection

def check_exchange(channel, exchangename, exchangetype):
    try:    
        channel.exchange_declare(exchangename, exchangetype, durable=True, passive=True) 
            # passive (bool): If set, the server will reply with Declare-Ok if the 
            # exchange already exists with the same name, and raise an error if not. 
            # The client can use this to check whether an exchange exists without 
            # modifying the server state.            
    except Exception as e:
        print('Exception:', e)
        return False
    return True

connection = create_connection()
channel = connection.channel()
#if the exchange is not yet created, exit the program
if not check_exchange(channel, exchangename, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)  # Exit with a success status
    
@app.route("/delete_bookings", methods=["DELETE"])
def delete_booking():
    data = request.get_json()
    print(data)
    delete_response = requests.delete("http://hotel_booking:5009/bookings/", json = data)
    print(delete_response)
    if delete_response.status_code == 200:
        print("delete operation was done...")
        result = delete_response.json()
        deleted_bookings = result["deleted_bookings"]
        print("sending email to inform user that their booking has been deleted...")
        for booking in deleted_bookings:
            print(booking)
            # TO-DO--> send the deleted booking as message to amqp broker, broker passes to 
            # email microservice when it comes online???
            email_to_send = {
                "email": booking["email"],
                "subject": "Booking Cancellation",
                "message": f"Your booking at {booking['hotel']} in {booking['city']} from {booking['checkin']} to {booking['checkout']} has been cancelled by the hotel admin."
            }
            channel.basic_publish(exchange=exchangename, routing_key="cancellation.email", 
            body=str(email_to_send), properties=pika.BasicProperties(delivery_mode = 2))
        return jsonify({"Cancelled_Bookings": deleted_bookings})
    else:
        return jsonify({"message": delete_response["message"]})
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)
