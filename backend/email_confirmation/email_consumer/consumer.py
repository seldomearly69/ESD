from flask import Flask
import pika, os, threading, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import amqp_connection
import time
import json

def on_message_received(ch,method,properties,body):
    print(f"Recieved message: {body}")

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.queue_declare(queue='email_q')

channel.basic_consume(queue='email_q', auto_ack=True, 
    on_message_callback=on_message_received)

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

print("Starting Consuming")

channel.start_consuming()
