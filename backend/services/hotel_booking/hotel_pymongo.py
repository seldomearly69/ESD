from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://ryanlee99324:BrImAqgUaXaNuEz6@esdproj.r2bp9gh.mongodb.net/Hotel'
mongo = PyMongo(app)


class Hotel:
    @staticmethod
    def json(booking):
        return {
            "username": booking["username"],
            "hotel": booking["hotel"],
            "city": booking["city"],
            "checkin": booking["checkin"],
            "checkout": booking["checkout"]
        }
    
@app.route("/")
def greeting():
    return jsonify({"code": 200, "message": "HEllo."}), 200
    
    
@app.route("/bookings/<string:userName>")
def find_bookings_by_username(userName):
    bookings = mongo.db.Hotel.find({"username": userName})
    
    if bookings:
        bookings_data = [Hotel.json(booking) for booking in bookings]
        return jsonify({"code": 200, "data": bookings_data})
    
    return jsonify({"code": 404, "message": "Bookings not found."}), 404


@app.route("/bookings/", methods=['POST'])
def create_hotel_booking():
    data = request.get_json()

    if mongo.db.Hotel.find_one({
        "username": data["username"],
        "hotel": data["hotel"],
        "city": data["city"],
        "checkin": data["checkin"],
        "checkout": data["checkout"]
    }):
        return jsonify({"code": 400, "data": {"booking": data}, "message": "Booking already exists."}), 400

    booking_id = mongo.db.Hotel.insert_one(data).inserted_id
    booking = mongo.db.Hotel.find_one({"_id": booking_id})

    return jsonify({"code": 201, "data": Hotel.json(booking)}), 201

@app.route("/bookings/", methods=['DELETE'])
def delete_bookings():
    data = request.get_json()

    city_name = data["city"]
    hotel_name = data["hotel"]
    dates = data["dates"]
        
    deleted_bookings_cursor = mongo.db.Hotel.find({"city": city_name, "hotel": hotel_name, "checkin": {"$in": dates}})
    deleted_bookings_data = [Hotel.json(booking) for booking in deleted_bookings_cursor]
    
    
    result = mongo.db.Hotel.delete_many({"city": city_name, "hotel": hotel_name, "checkin": {"$in": dates}})

    if result.deleted_count > 0:
        return jsonify({"deleted_bookings": deleted_bookings_data}), 200

    return jsonify({"message": "No matching bookings found."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)
