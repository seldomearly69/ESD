from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime
import json
app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://ryanlee99324:BrImAqgUaXaNuEz6@esdproj.r2bp9gh.mongodb.net/flight'
mongo = PyMongo(app)


class Hotel:
    @staticmethod
    def json(booking):
        return {
            "username": booking["username"],
            "flight_no": booking["flight_no"],
            "airline": booking["airline"],
            "departure_city": booking["departure_city"],
            "arrival_city": booking["arrivial_city"],
            "departure": booking["departure"],
            "arrival": booking["arrival"]
        }
    
def customEncoder(o):
    if isinstance(o, ObjectId):
        return str(o)
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError(f'Object of type {o.__class__.__name__} is not JSON serializable')
@app.route("/all_flights")
def get_all():
    allRecords = mongo.db.flight.find()

    try:
        # Convert all records to a list of dicts with JSON serializable ObjectId
        records = json.loads(json.dumps([record for record in allRecords], default=customEncoder))

        if records:
            return jsonify(records)

        return jsonify(
            {
                "code": 404,
                "message": "There are no records."
            }
        ), 404
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": str(e)
            }
        ), 500

#Find Booking
@app.route("/flight/<ObjectId:_id>")
def find_booking(_id):
    r = mongo.db.flight.find_one({"_id": _id})
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


#Create Record
@app.route("/flight/<ObjectId:_id>", methods=['POST'])
def create_record(_id):
    r = mongo.db.flight.find_one({"_id": _id})
    if r:
        return jsonify({"code": 400, "message": "Record already exists for this user. Use PUT method if you are trying to update the record."}), 400

    data = request.get_json()
    data['_id'] = _id
    mongo.db.flight.insert_one(data)
    return jsonify(
        {
            "code": 201, 
            "data": data
        }
    ), 201


#Update Record
@app.route("/flight/<ObjectId:_id>", methods=['PUT'])
def update_record(_id):
    r = mongo.db.flight.find_one(
        {
            "_id": _id
        }
        )
    if not r:
        return jsonify(
            {
                "code": 400, 
                "message": "Record does not exist for this user. Use POST to create a new record."
            }
            ), 400

    data = request.get_json()
    mongo.db.flight.update_one({"_id": _id}, {"$set": data})
    return jsonify(
        {
            "code": 201, 
            "data": r
        }
    ), 201



#Delete Record
@app.route("/flight/<ObjectId:_id>", methods=['DELETE'])
def delete_record(_id):
    r = mongo.db.flight.find_one({"_id": _id})
    if not r:
        return jsonify(
            {
                "code": 400, 
                "message": "Record does not exist for this user."
            }
        ), 400

    mongo.db.flight.delete_one({"_id": _id})
    return jsonify(
        {
            "code": 201, 
            "data": r, "message": "Deleted successfully!"
        }
    ), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)
