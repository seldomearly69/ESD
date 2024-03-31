from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson import ObjectId
from datetime import datetime
import json
from flasgger import Swagger

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://ryanlee99324:BrImAqgUaXaNuEz6@esdproj.r2bp9gh.mongodb.net/flight'
mongo = PyMongo(app)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SWAGGER'] = {
    'title': 'Flight API',
    'uiversion': 3,
    'description':"Allows get, create, update and delete operations for flight records"
}
swagger = Swagger(app)
    
def customEncoder(o):
    if isinstance(o, ObjectId):
        return str(o)
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError(f'Object of type {o.__class__.__name__} is not JSON serializable')


@app.route("/all_flights")
def get_all():
    """
    Get all flights
    ---
    tags:
      - Flights
    responses:
      200:
        description: A list of flights

      404:
        description: No flights found

    """
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

    """
    Find a flight booking by ID
    ---
    tags:
      - Flights
    parameters:
      - name: _id
        in: path
        type: string
        required: true
        description: The ID of the flight booking to find
    responses:
      200:
        description: A flight booking found with the given ID
     
      404:
        description: Record not found
    """

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


    """
    Create a new flight record
    ---
    tags:
      - Flights
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: flight
        description: The flight to create
        required: true
        schema:
          type: object
          required:
            - departure
            - arrival
            - dayTime
            - email
          properties:
            _id:
              type: object
              properties:
                $oid:
                  type: string
                  example: "6600265a42049415b3b52a2d"
            departure:
              type: object
              properties:
                airline_logo:
                  type: string
                  example: "https://www.gstatic.com/flights/airline_logos/70px/UA.png"
                carbon_emissions:
                  type: object
                  properties:
                    difference_percent:
                      type: integer
                      example: -15
                    this_flight:
                      type: integer
                      example: 1108000
                    typical_for_this_route:
                      type: integer
                      example: 1303000
                departure_token:
                  type: string
                  example: "WyJDalJJUVVoYVNWZHNRMUJwYkhOQlJWaEpjSGRDUnkwdExTMHRMUzB..."
                flights:
                  type: array
                  items:
                    type: object
                    properties:
                      airline:
                        type: string
                        example: "United"
                      # Define other properties as shown in your JSON...
                layovers:
                  type: array
                  items:
                    type: object
                    properties:
                      duration:
                        type: integer
                        example: 109
                      id:
                        type: string
                        example: "SFO"
                      name:
                        type: string
                        example: "San Francisco International Airport"
                price:
                  type: integer
                  example: 2040
                total_duration:
                  type: integer
                  example: 1213
                type:
                  type: string
                  example: "Round trip"
            arrival:
              type: object
              # Define the properties similar to departure...
            dayTime:
              type: string
              example: "2024-03-24T13:10:49.935Z"
            email:
              type: string
              example: "abc@gmail.com"
    responses:
      201:
        description: Flight record created
      400:
        description: Record already exists or invalid input
    """


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
    """
    Update an existing flight record
    ---
    tags:
      - Flights
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: flight
        description: The flight to create
        required: true
        schema:
          type: object
          required:
            - departure
            - arrival
            - dayTime
            - email
          properties:
            _id:
              type: object
              properties:
                $oid:
                  type: string
                  example: "6600265a42049415b3b52a2d"
            departure:
              type: object
              properties:
                airline_logo:
                  type: string
                  example: "https://www.gstatic.com/flights/airline_logos/70px/UA.png"
                carbon_emissions:
                  type: object
                  properties:
                    difference_percent:
                      type: integer
                      example: -15
                    this_flight:
                      type: integer
                      example: 1108000
                    typical_for_this_route:
                      type: integer
                      example: 1303000
                departure_token:
                  type: string
                  example: "WyJDalJJUVVoYVNWZHNRMUJwYkhOQlJWaEpjSGRDUnkwdExTMHRMUzB..."
                flights:
                  type: array
                  items:
                    type: object
                    properties:
                      airline:
                        type: string
                        example: "United"
                      # Define other properties as shown in your JSON...
                layovers:
                  type: array
                  items:
                    type: object
                    properties:
                      duration:
                        type: integer
                        example: 109
                      id:
                        type: string
                        example: "SFO"
                      name:
                        type: string
                        example: "San Francisco International Airport"
                price:
                  type: integer
                  example: 2040
                total_duration:
                  type: integer
                  example: 1213
                type:
                  type: string
                  example: "Round trip"
            arrival:
              type: object
              # Define the properties similar to departure...
            dayTime:
              type: string
              example: "2024-03-24T13:10:49.935Z"
            email:
              type: string
              example: "abc@gmail.com"
    responses:
      201:
        description: Flight record updated
      400:
        description: Record does not exist for this ID or invalid input
    """
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
    """
    Delete a flight record
    ---
    tags:
      - Flights
    parameters:
      - name: _id
        in: path
        type: string
        required: true
        description: The ID of the flight to delete
    responses:
      201:
        description: Flight record deleted successfully
      400:
        description: Record does not exist for this ID
    """

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
