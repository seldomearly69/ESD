from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import pika
import time, sys

import json
import time
import sys

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})



#Email part
hostname = "rabbitmq" # default hostname
port = 5672            # default port
user="username"
password="password"
exchangename = "email_exchange" 
exchangetype = "topic"

headers = {'Content-Type': 'application/json'}

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
    
def publish_to_broker(msg):
    
    message = ""
    email = ""
    if "hotel" in msg:
        Hbooking = msg["hotel"]
        message +=  f"Your booking at {Hbooking['hotel']} from {Hbooking['check_in_date']} to {Hbooking['check_out_date']} has been confirmed.\n\n"
        email += Hbooking["email"]
    if "flight" in msg:
        Fbooking =  msg["flight"]
        message +=  f"Your Flight Booking has been confirmed too!"
        
    email_to_send = {
            "email": email,
            "subject": "Booking Confirmation",
            "message": message
    }
    print(message)
    if email and message:
        channel.basic_publish(exchange=exchangename, routing_key="confirmation.email", 
        body=str(email_to_send), properties=pika.BasicProperties(delivery_mode = 2))
            
    
    
    

@app.route("/search", methods = ["POST"])
def search():
    data = request.get_json()
    print(data,flush=True)
    if data["engine"] == "google_flights":
        print(1,flush=True)
        url = "http://host.docker.internal:5007/flights"
    else:
        url = "http://host.docker.internal:5003/hotels"
    
    response = requests.post(url, json = data)
    print(1,flush=True)
    if (response.status_code == 200):
        print(response,flush=True)
        return jsonify(response.json()), 200
    else:
        return jsonify("An error occurred"), response.status_code

@app.route("/payment", methods=["POST"])
def make_payment():

    data = request.get_json()
    amt = data["amount"]
    
    payment_service_url = "http://host.docker.internal:5020/create_payment_intent"  # assuming docker compose is run and payment service name is set to payment
   
    response = requests.post(payment_service_url, json.dumps({"amount": amt}), headers=headers)

    if response.status_code == 200:
        client_secret = response.json().get('clientSecret')
        return jsonify({"clientSecret": client_secret}), 200
    else:
        return jsonify({"error": "Failed to create payment intent"}), response.status_code

    

# Once payment is made send booking details to hotel_booking / flights service
@app.route("/confirm_booking", methods = ["POST"])
def confirm_booking():
    print(1,flush=True)
    data = request.get_json()
    print(2,flush=True)
    
    msg_to_broker = {}
    print(3,flush=True)
    if ("flight" in data):
        print(1,flush=True)
        fBooking = data["flight"]
        fBooking["dayTime"] = data["dayTime"]
        fBooking["email"] = data["email"]
        response = requests.post("http://host.docker.internal:5005/flight", json.dumps(fBooking), headers = headers)
        result = response.json()
        if response.status_code == 201:
            msg_to_broker["flight"] = result["data"]
        # Send flight booking confirmation msg to rabbitMq
        if response.status_code != 201:
            return jsonify({"message": "Error inserting into flight booking"}), response.status_code

    if ("hotel" in data):
        print(4,flush=True)
        hBooking = {}
        hBooking["hotel"] = data["hotel"]["hotel"]["name"]
        hBooking["address"] = data["hotel"]["hotel"]["gps_coordinates"]
        hBooking["check_in_date"] = data["hotel"]["hotel"]["stay"][0]
        hBooking["check_out_date"] = data["hotel"]["hotel"]["stay"][1]
        hBooking["num_rooms"] = data["hotel"]["hotel"]['num_rooms']
        hBooking["price"] = "temp_val"
        hBooking["date"] = data["dayTime"]
        hBooking["email"] = data["email"]
        hBooking["check_in_time"] = "temp_val"
        hBooking["check_out_time"] = "temp_val"
        response = requests.post("http://host.docker.internal:5009/bookings", json.dumps(hBooking), headers = headers)
        result = response.json()
        hotel_bking= result['data'] 
        # Send hotel booking confirmation msg to rabbitMq
        if response.status_code == 201:
            msg_to_broker["hotel"] = hotel_bking
        if response.status_code != 201:
            return jsonify({"message": "Error inserting into hotel booking"}),response.status_code
    
    if msg_to_broker:
        publish_to_broker(msg_to_broker)

    return jsonify(
        {
            "code": 201,
            "data": data
        }
    ), 201





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008, debug=True)