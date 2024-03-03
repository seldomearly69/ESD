import requests

# Set the URL of your Flask app
url = 'http://127.0.0.1:5001/hotel/4'  # Adjust the URL accordingly

# Send a DELETE request to delete the record
response = requests.delete(url)

# Check the response status
if response.status_code == 204:
    print("Record deleted successfully!")
elif response.status_code == 404:
    print("Record not found.")
else:
    print(f"Failed to delete record. Status code: {response.status_code}")
    print(response.text)
