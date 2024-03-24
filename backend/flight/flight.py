from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson import ObjectId
from datetime import datetime
import json

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://ryanlee99324:BrImAqgUaXaNuEz6@esdproj.r2bp9gh.mongodb.net/flight'
mongo = PyMongo(app)
CORS(app, resources={r"/*": {"origins": "*"}})
    
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
@app.route("/flight/<string:_id>")
def find_booking(_id):

    try:
        r = mongo.db.flight.find_one({"_id" : ObjectId(_id)})
        r["_id"] = str(r["_id"])
        return jsonify(
            {
                "code": 200, 
                "data": r
            }
        )
    except Exception as e:
        return jsonify(
                {
                    "code": 404,
                    "error": str(e),
                    "message": "Record not found"
                }
            ), 404
    
    
    


#Create Record
@app.route("/flight", methods=['POST'])
def create_record():
    data = request.get_json()
    r = mongo.db.flight.find_one(data)
    if r:
        return jsonify({"code": 400, "message": "Record already exists. Use PUT method if you are trying to update the record."}), 400

    
    mongo.db.flight.insert_one(data)
    data["_id"] = customEncoder(data["_id"])
    return jsonify(
        {
            "code": 201,
            "data": data
        }
    ), 201


#Update Record
@app.route("/flight/<string:_id>", methods=['PUT'])
def update_record(_id):
    data = request.get_json()
    try:
        r = mongo.db.flight.find_one({"_id" : ObjectId(_id)})
        mongo.db.flight.update_one({"_id": ObjectId(_id)}, {"$set": data})
        data["_id"] = str(r["_id"])
        return jsonify(
            {
                "code": 201, 
                "data": data
            }
        ), 201
    except Exception as e:
        return jsonify(
            {
                "code": 400, 
                "message": "Record does not exist for this user. Use POST to create a new record.",
                "error": str(e)
            }
            ), 400

    



#Delete Record
@app.route("/flight/<string:_id>", methods=['DELETE'])
def delete_record(_id):

    r = mongo.db.flight.delete_one({"_id": ObjectId(_id)})
    if r.deleted_count== 1:
        return jsonify(
            {
                "code": 201, 
                "message": "Deleted successfully!"
            }
        ), 201
    return jsonify(
        {
            "code": 400, 
            "message": "Record does not exist for this user."
        }
    ), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
