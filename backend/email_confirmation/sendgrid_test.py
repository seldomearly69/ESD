import requests
import json

# SendGrid API key
sendgrid_api_key = 'your_sendgrid_api_key'

# Function to send a test email using SendGrid
def send_test_email():
    url = "https://api.sendgrid.com/v3/mail/send"
    headers = {
        "Authorization": f"Bearer {sendgrid_api_key}",
        "Content-Type": "application/json"
    }

    # Test email content
    email_content = {
        "personalizations": [
            {
                "to": [{"email": "recipient@example.com"}],  # Replace with recipient email
                "subject": "Test Email from SendGrid"
            }
        ],
        "from": {"email": "sender@example.com"},  # Replace with sender email
        "content": [
            {
                "type": "text/plain",
                "value": "This is a test email from SendGrid. If you received this, it means the SendGrid API integration is working properly."
            }
        ]
    }

    # Send email
    response = requests.post(url, headers=headers, json=email_content)
    if response.status_code == 202:
        print("Test email sent successfully.")
    else:
        print("Failed to send test email.")

if __name__ == "__main__":
    send_test_email()
