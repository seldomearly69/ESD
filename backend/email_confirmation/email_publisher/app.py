from flask import Flask, request, jsonify
import pika
import os
import amqp_connection



app = Flask(__name__)

connection=amqp_connection.create_connection()
channel=connection.channel()
@app.route('/publish', methods=['POST'])
def publish():
    message = request.json
    # Publish message
    channel.basic_publish(exchange='email_exchange',
                          routing_key='confirmation.email',
                          body=str(message),
                          properties=pika.BasicProperties(
                             delivery_mode=2,  # make message persistent
                          ))

    connection.close()
    return jsonify({"status": "success", "message": "Email request published"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
