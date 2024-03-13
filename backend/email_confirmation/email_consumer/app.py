from flask import Flask
import pika, os, threading, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import amqp_connection
import time
import json

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
    server.login(msg['From'], os.getenv('aggy eynw nrpv vcqc'))
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()

def callback(ch, method, properties, body):

        
        email_data = json.loads(body.decode('utf-8'))  # Assuming JSON is used for message serialization
        print(email_data)
        send_email(email_data['email'], email_data['subject'], email_data['message'])
        print()
        


def start_consuming(channel):
    tries=0
    while tries<=12:
        try:
            channel.basic_consume(queue='email_queue', on_message_callback=callback,auto_ack=True)
            channel.start_consuming()
        except:
            print("Cannot connect. Trying again")
            tries+=1
            time.sleep(5)
@app.route('/')
def index():
    return "Email Consumer Running"

if __name__ == '__main__':
    connection=amqp_connection.create_connection()
    channel=connection.channel()
    start_consuming(channel)
    app.run(debug=True, host='0.0.0.0', port=5001)

