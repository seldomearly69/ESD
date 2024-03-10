from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/hoteldb"
mongo = PyMongo(app)

# Assuming you have a collection named 'hotel_bookings' in your MongoDB database

@app.route("/all_hotels")
def get_all():
    allRecords = mongo.db.hotel_bookings.find()

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
    r = mongo.db.hotel_bookings.find_one({"booking_id": booking_id})

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
    r = mongo.db.hotel_bookings.find_one({"booking_id": booking_id})
    if r:
        return jsonify(
            {
                "code": 400,
                "message": "Record already exists for this user. Use PUT method if you are trying to update the record."
            }
        ), 400

    data = request.get_json()
    data['booking_id'] = booking_id
    mongo.db.hotel_bookings.insert_one(data)

    return jsonify(
        {
            "code": 201,
            "data": data
        }
    ), 201

@app.route("/hotel/<int:booking_id>", methods=['PUT'])
def update_record(booking_id):
    r = mongo.db.hotel_bookings.find_one({"booking_id": booking_id})
    if not r:
        return jsonify(
            {
                "code": 400,
                "message": "Record does not exist for this user. Use POST to create a new record."
            }
        ), 400

    data = request.get_json()
    mongo.db.hotel_bookings.update_one({"booking_id": booking_id}, {"$set": data})

    return jsonify(
        {
            "code": 201,
            "data": r
        }
    ), 201

@app.route("/hotel/<int:booking_id>", methods=['DELETE'])
def delete_record(booking_id):
    r = mongo.db.hotel_bookings.find_one({"booking_id": booking_id})
    if not r:
        return jsonify(
            {
                "code": 400,
                "message": "Record does not exist for this user."
            }
        ), 400

    mongo.db.hotel_bookings.delete_one({"booking_id": booking_id})

    return jsonify(
        {
            "code": 201,
            "data": r,
            "message": "Deleted successfully!"
        }
    ), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
