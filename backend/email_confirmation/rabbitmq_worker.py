import pika
import json
import requests

# RabbitMQ Connection Parameters
rabbitmq_host = 'localhost'
rabbitmq_port = 5672
rabbitmq_queue = 'flight_bookings'

# SendGrid API key
sendgrid_api_key = 'your_sendgrid_api_key'

# Function to send email using SendGrid
def send_email(booking_details):
    url = "https://api.sendgrid.com/v3/mail/send"
    headers = {
        "Authorization": f"Bearer {sendgrid_api_key}",
        "Content-Type": "application/json"
    }

    # Construct email content
    email_content = {
        "personalizations": [
            {
                "to": [{"email": booking_details['email']}],
                "subject": "Flight Booking Confirmation"
            }
        ],
        "from": {"email": "noreply@example.com"},
        "content": [
            {
                "type": "text/plain",
                "value": f"Dear {booking_details['username']},\n\nYour flight from {booking_details['departure_city']} to {booking_details['arrival_city']} has been booked successfully.\n\nFlight Details:\nFlight No: {booking_details['flight_no']}\nAirline: {booking_details['airline']}\nDeparture Time: {booking_details['departure']}\nArrival Time: {booking_details['arrival']}"
            }
        ]
    }

    # Send email
    response = requests.post(url, headers=headers, json=email_content)
    if response.status_code == 202:
        print("Email sent successfully.")
    else:
        print("Failed to send email.")

# Function to consume messages from RabbitMQ queue
def callback(ch, method, properties, body):
    try:
        booking_details = json.loads(body)
        send_email(booking_details)  # Send confirmation email
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

# Establish connection with RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port))
channel = connection.channel()

# Declare queue
channel.queue_declare(queue=rabbitmq_queue, durable=True)

# Set prefetch count to 1
channel.basic_qos(prefetch_count=1)

# Start consuming messages
channel.basic_consume(queue=rabbitmq_queue, on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

