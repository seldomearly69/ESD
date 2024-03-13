from flask import Flask, request, jsonify
import pika
import os
import amqp_connection

connection=amqp_connection.create_connection()
channel=connection.channel()

app = Flask(__name__)


@app.route('/publish', methods=['POST'])
def publish():
    if request.is_json:
        try:
            email = request.get_json()
            print(email)
                # Publish message
            channel.basic_publish(exchange='email_exchange',
                          routing_key='confirmation.email',
                          body=str(email),
                          properties=pika.BasicProperties(
                             delivery_mode=2,  # make message persistent
                          ))

    
            return jsonify({"status": "success", "message": email}), 200
            

        except Exception as e:
          

            return jsonify({
                "code": 500,
                "message": "internal error: "
            }), 500
    


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
