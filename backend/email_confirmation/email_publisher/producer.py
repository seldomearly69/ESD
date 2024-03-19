import pika
import json

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.queue_declare(queue='email_q')

message = 'Test'

channel.basic_publish(exchange='', routing_key='email_q', body = message)

print(f"send message: {message}")

connection.close()