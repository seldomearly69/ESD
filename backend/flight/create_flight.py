import requests
import json

# Set the URL of your Flask app
url = 'http://127.0.0.1:5002/flight/1'  # Update the URL accordingly

# Sample data for creating a new flight booking record
data = {
    "username": "john_doe",
    "flight_no": 123,
    "airline": "Sample Airlines",
    "departure_city": "City A",
    "arrival_city": "City B",
    "departure": "2024-03-03T10:00:00",  # Format: YYYY-MM-DDTHH:MM:SS
    "arrival": "2024-03-03T14:30:00"
}

# Send a POST request to create a new record
response = requests.post(url, json=data)

# Check the response status
print(f"Status Code: {response.status_code}")

# Print the response content (for debugging)
print("Response Content:", response.text)

# Try to parse JSON (handle the exception)
try:
    json_response = response.json()
    print("Parsed JSON Response:", json_response)
except json.decoder.JSONDecodeError as e:
    print(f"Failed to parse JSON: {e}")
