from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import amqp_connection
import time
import json

queue_name="email_queue"
booking_email = "esdt04g6@gmail.com"
app_password = "alzqxkgqkzetuhbk"

def send_email(recipient, subject, body):
    try:
        # Create message container
        msg = MIMEMultipart()
        msg['From'] = booking_email
        msg['To'] = recipient
        msg['Subject'] = subject

        # Add body to email
        msg.attach(MIMEText(body, 'plain'))

        # Establish SMTP connection
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(booking_email, app_password)
            server.sendmail(booking_email, recipient, msg.as_string())

        print("Email sent successfully!")
    except Exception as e:
        print("An error occurred while sending the email:", e)

def callback(ch, method, properties, body):

        print(body)
        corrected_body = body.decode('utf-8').replace("'", '"')
        email_data = json.loads(corrected_body) # Assuming JSON is used for message serialization
        print(email_data)
        send_email(email_data['email'], email_data['subject'], email_data['message'])
        
        
def start_consuming(channel):
    tries=0
    while tries<=12:
        try:
            channel.basic_consume(queue='email_queue', on_message_callback=callback,auto_ack=True)
            channel.start_consuming()
        except Exception as e:
            print("Cannot connect. Trying again...")
            print(e)
            tries+=1
            time.sleep(5)
    
if __name__ == '__main__':
    print("activity_log: Getting Connection")
    connection=amqp_connection.create_connection()
    print("activity_log: Connection established successfully")
    channel=connection.channel()
    start_consuming(channel)