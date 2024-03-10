from flask import Flask, jsonify
import requests



app = Flask(__name__)

@app.route('/send', methods=['GET'])
def send_email():
    # Define the payload for the test email
    test_email_data = {
        "email": "ryanlee99324@gmail.com",
        "subject": "Test Email",
        "message": "This is a test email sent from the send_test_email service."
    }
    
    # URL of the email_publisher service endpoint
    publisher_url = 'http://email_publisher:5002/publish'
    
    # Send a POST request to the email_publisher service
    response = requests.post(publisher_url, json=test_email_data)
    
    # Return the response from the email_publisher service
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
