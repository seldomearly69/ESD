from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import pika
import time, sys

import json
import time
import sys

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})


@app.route("/search")
def search():
    data = request.get_json()
    fresponse = None
    hresponse = None
    if "flight" in data:
        fresponse = requests.get("http://flight_search:5007/flights", json = data["flight"])
        if (fresponse.status_code == 200):
            fresponse = fresponse.json()

    if "hotel" in data:
        hresponse = requests.get("http://hotel_search:5003/hotels", json = data["hotel"])
        if (hresponse.status_code == 200):
            hresponse = hresponse.json()

    return jsonify({"flight": fresponse, "hotel": hresponse})

@app.route("/payment", methods=["POST"])
def make_payment():
    data = request.get_json()
    amt = data["amount"]

    # requests.post("", json.dumps({"amount": amt, "currency": "sgd"}))
    # TO-DO:
    #     Send amount for payment
    #     Send flight booking to database
    #     Send hotel booking to database


    payment_service_url = "http://payment/create_payment_intent"  # assuming docker compose is run and payment service name is set to payment

   
    response = requests.post(payment_service_url, json={"amount": amt})

    if response.status_code == 200:
       
        client_secret = response.json().get('clientSecret')
        return jsonify({"clientSecret": client_secret}), 200
    else:
        return jsonify({"error": "Failed to create payment intent"}), response.status_code

    

@app.route("/confirm_booking", methods = ["POST"])
def confirm_booking():
    data = request.get_json()
    if ("flight" in data):
        fBooking = {"departure": data["flight"][0]}

        if len(data["flight"] == 2):
            fBooking["arrival"] = data["flight"][1]
        
        response = requests.post("http://flights:5000/flight",json.dumps(fBooking))
        if response.status_code != 201:
            raise Exception("Something went wrong with flight booking")
    
    if ("hotel" in data):
        hBooking = data["hotel"]
        response = requests.post("http://hotel_booking:5009/bookings", hBooking)
        if response.status_code != 201:
            raise Exception("Something went wrong with hotel booking")
    
    
    return jsonify(
        {
            "code": 201,
            "data": data
        }
    ), 201



#Email part
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

#Email
connection = create_connection()
channel = connection.channel()
#if the exchange is not yet created, exit the program
if not check_exchange(channel, exchangename, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)  # Exit with a success status
    
@app.route("/create_booking", methods=["POST"])
def email_confirmation():
    data = request.get_json()
    print(data)
    booking_response = requests.post("http://hotel_booking:5009/bookings/", json = data)
    print(booking_response)
    if booking_response.status_code == 201:
        print("Booking operation was done...")
        result = booking_response.json()
        booking = result['data'] 
        print(booking)
        print("sending email")
        if booking['hotel']:
            # TO-DO--> send the deleted booking as message to amqp broker, broker passes to 
            # email microservice when it comes online???
            email_to_send = {
                "email": booking["email"],
                "subject": "Booking Confirmation",
                "message": f"Your booking at {booking['hotel']} in {booking['city']} from {booking['checkin']} to {booking['checkout']} has been confirmed."
            }
            channel.basic_publish(exchange=exchangename, routing_key="confirmation.email", 
            body=str(email_to_send), properties=pika.BasicProperties(delivery_mode = 2))
            return jsonify({"message": booking})
    
        else:
         # TO-DO--> send the deleted booking as message to amqp broker, broker passes to 
            # email microservice when it comes online???
            email_to_send = {
                "email": booking["email"],
                "subject": "Booking Confirmation",
                "message": f"Your flight {booking['flight_no']} from {booking['departure_city']} to {booking['arrival_city']} on {booking['departure']} has been confirmed."
            }
            channel.basic_publish(exchange=exchangename, routing_key="confirmation.email", 
            body=str(email_to_send), properties=pika.BasicProperties(delivery_mode = 2))
            return jsonify({"message": booking})
    else:
        return jsonify({"message": "Booking Failed"})
    
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008, debug=True)