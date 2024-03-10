from flask import Flask, request, jsonify
import pika
import os



app = Flask(__name__)

@app.route('/publish', methods=['POST'])
def publish():
    message = request.json
    # Establish a connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv("RABBITMQ_HOST", "localhost")))
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue='emailQueue', durable=True)

    # Publish message
    channel.basic_publish(exchange='',
                          routing_key='emailQueue',
                          body=str(message),
                          properties=pika.BasicProperties(
                             delivery_mode=2,  # make message persistent
                          ))

    connection.close()
    return jsonify({"status": "success", "message": "Email request published"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
