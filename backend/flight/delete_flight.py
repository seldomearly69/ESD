import requests

# Set the URL of your Flask app
url = 'http://127.0.0.1:5002/flight/1'  # Adjust the URL accordingly

# Send a DELETE request to delete the record with booking_id=1
response = requests.delete(url)

# Check the response status and content
if response.status_code == 201:
    print("Record deleted successfully!")
    print(response.json())

else:
    print(f"Failed to delete record. Status code: {response.status_code}")
    print(response.json())
