from flask import Flask, request, jsonify
from flask_cors import CORS

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import ObjectId


import time
import sys

app = Flask(__name__)
CORS(app)

def connect_to_db():
    max_retries = 30
    retries = 0

#apBxz258V1HCEmEb

    while retries < max_retries:
        try:
            # Update the MongoDB connection details
            client = MongoClient('mongodb+srv://brendan:apBxz258V1HCEmEb@esd.qq3dsm4.mongodb.net/?retryWrites=true&w=majority&appName=ESD')
            # Try to run a simple command to check if the database is reachable
            client.admin.command('ping')
            print("Database is reachable.")
            return client
        except ConnectionFailure as e:
            print(e)
            print(f"Database not ready yet. Retrying... ({retries}/{max_retries})")
            retries += 1
            time.sleep(1)

    print("Failed to connect to the database after retries. Exiting.")
    sys.exit(1)

client = connect_to_db()
db = client["hoteldb"]
coll = db["hoteldb"]

@app.route("/all_hotels")
def get_all():
    allRecords = client.db.hotel_bookings.find()

    if allRecords.count():
        return jsonify([record for record in allRecords])

    return jsonify(
        {
            "code": 404,
            "message": "There are no records."
        }
    ), 404

@app.route("/hotel/<int:booking_id>")
def find_booking(booking_id):
    r = client.db.hotel_bookings.find_one({"booking_id": booking_id})

    if r:
        return jsonify(
            {
                "code": 200,
                "data": r
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Record not found."
        }
    ), 404

@app.route("/hotel/<int:booking_id>", methods=['POST'])
def create_record(booking_id):
    r = client.db.hotel_bookings.find_one({"booking_id": booking_id})
    if r:
        return jsonify(
            {
                "code": 400,
                "message": "Record already exists for this user. Use PUT method if you are trying to update the record."
            }
        ), 400

    data = request.get_json()
    data['booking_id'] = booking_id
    client.db.hotel_bookings.insert_one(data)

    return jsonify(
        {
            "code": 201,
            "data": data
        }
    ), 201

@app.route("/hotel/<int:booking_id>", methods=['PUT'])
def update_record(booking_id):
    r = client.db.hotel_bookings.find_one({"booking_id": booking_id})
    if not r:
        return jsonify(
            {
                "code": 400,
                "message": "Record does not exist for this user. Use POST to create a new record."
            }
        ), 400

    data = request.get_json()
    client.db.hotel_bookings.update_one({"booking_id": booking_id}, {"$set": data})

    return jsonify(
        {
            "code": 201,
            "data": r
        }
    ), 201

@app.route("/hotel/<int:booking_id>", methods=['DELETE'])
def delete_record(booking_id):
    r = client.db.hotel_bookings.find_one({"booking_id": booking_id})
    if not r:
        return jsonify(
            {
                "code": 400,
                "message": "Record does not exist for this user."
            }
        ), 400

    client.db.hotel_bookings.delete_one({"booking_id": booking_id})

    return jsonify(
        {
            "code": 201,
            "data": r,
            "message": "Deleted successfully!"
        }
    ), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
