from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson import ObjectId
from flasgger import Swagger
import os

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://ryanlee99324:BrImAqgUaXaNuEz6@esdproj.r2bp9gh.mongodb.net/Hotel'
# Initialize flasgger 
app.config['SWAGGER'] = {
    'title': 'hotel_booking service API',
    'version': 1.0,
    "openapi": "3.0.2",
    'description': 'Allows create, retrieve, and delete of hotels'
}

mongo = PyMongo(app)
swagger_template_path = os.path.join(os.getcwd(), 'hotel_booking.yml')
swagger = Swagger(app, template_file=swagger_template_path)

CORS(app, resources={r"/*": {"origins": "*"}})

class Hotel:
    @staticmethod
    def json(booking):
        return {
            "email": booking["email"],
            "hotel": booking["hotel"],
            "address": booking["address"],
            "num_rooms": booking["num_rooms"],
            "price": booking["price"],
            "check_in_date": booking["check_in_date"],
            "check_in_time": booking["check_in_time"],
            "check_out_date": booking["check_out_date"],
            "check_out_time": booking["check_out_time"],
            "date" : booking["date"]
        }
    

@app.route("/bookings/<string:email>")
def find_bookings_by_username(email):
    bookings = mongo.db.Hotel.find({"email": email})
    
    if bookings:
        bookings_data = [Hotel.json(booking) for booking in bookings]
        return jsonify({"code": 200, "data": bookings_data})
    
    return jsonify({"code": 404, "message": "Bookings not found."}), 404


@app.route("/bookings", methods=['POST'])
def create_hotel_booking():
    
    data = request.get_json()
    print(data,flush=True)
    if mongo.db.Hotel.find_one(data):
        return jsonify({"code": 400, "data": {"booking": data}, "message": "Booking already exists."}), 400

    booking_id = mongo.db.Hotel.insert_one(data).inserted_id
    print(booking_id, type(booking_id))
    booking = mongo.db.Hotel.find_one({'_id':booking_id})
    print(booking)
    return jsonify({"code": 201, "data": Hotel.json(booking)}), 201


@app.route("/bookings", methods=['DELETE'])
def delete_bookings():
    print(1,flush=True)
    data = request.get_json()
    print(2,flush=True)
    print(data)
    hotel_name = data["hotel"]
    dates = data["dates"]
    criteria = [{"check_in_date": {"$in": dates}},{"check_out_date": {"$in": dates}},{"check_in_date": {"$nin": dates},"check_out_date": {"$nin": dates}}]
    to_delete = []
    to_delete += [booking for booking in mongo.db.Hotel.find({"hotel": hotel_name, "$or": criteria})]
    if len(to_delete)== 0:
        return jsonify({"message": "No matching bookings found."}), 404

    for b in to_delete:
        b["_id"] = str(b["_id"])

    result = mongo.db.Hotel.delete_many({"hotel": hotel_name, "$or": criteria})
    return jsonify({"deleted_bookings": to_delete}), 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)
