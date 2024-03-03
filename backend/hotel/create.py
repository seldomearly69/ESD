import requests
from datetime import datetime

# Set the URL of your Flask app
url = 'http://127.0.0.1:5001/hotel/1'  # Adjust the URL accordingly

# Data for the new hotel booking
data = {
    "username": "john_doe",
    "hotel": "Grand Hotel",
    "city": "New York",
    "checkin": "2022-03-03T14:00:00",
    "checkout": "2022-03-05T12:00:00"
}

# Send a POST request to create a new record
response = requests.post(url, json=data)

# Check the response status and content
if response.status_code == 201:
    print("Record created successfully!")
    print(response.json())
else:
    print(f"Failed to create record. Status code: {response.status_code}")
    print(response.json())
