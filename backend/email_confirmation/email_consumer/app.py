from flask import Flask
import pika, os, threading, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import amqp_connection

queue_name="email_queue"

app = Flask(__name__)

def send_email(recipient, subject, body):
    msg = MIMEMultipart()
    msg['From'] = os.getenv('booking.t4.g6@gmail.com')
    msg['To'] = recipient
    msg['Subject'] = subject
    message = body
    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)  
    server.starttls()
    server.login(msg['From'], os.getenv('aggyeynwnrpvvcqc'))
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()

def callback(ch, method, properties, body):
    email_data = eval(body.decode('utf-8'))
    send_email(email_data['email'], email_data['subject'], email_data['message'])
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consuming(channel):
    
    
    channel.basic_consume(queue='email_queue', on_message_callback=callback)
    channel.start_consuming()

@app.route('/')
def index():
    return "Email Consumer Running"

if __name__ == '__main__':
    connection=amqp_connection.create_connection()
    channel=connection.channel()
    start_consuming(channel)
    app.run(debug=True, host='0.0.0.0', port=5001)

