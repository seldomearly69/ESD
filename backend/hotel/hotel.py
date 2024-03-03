from flask import Flask,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/hoteldb'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
app.app_context().push()

#Hotel Bookings Table
class Hotel_booking(db.Model):
    booking_id = db.Column("id",db.Integer, primary_key=True)
    username = db.Column("username", db.String(100))
    hotel = db.Column("hotel", db.String(100))
    city = db.Column("city", db.String(100))
    checkin = db.Column("checkin", db.DateTime)
    checkout = db.Column("checkout", db.DateTime)

    def __init__(self,booking_id, username, hotel, city, checkin, checkout):
        self.booking_id
        self.username = username
        self.hotel  = hotel
        self.city = city
        self.checkin = checkin
        self.checkout = checkout

    def __repr__(self):
        return f'<Username: {self.username}> - <BookingId: {self.booking_id}>'

@app.route("/all_hotels")
def get_all():
    allRecords = Hotel_booking.query.all()

    if len(allRecords):
        return jsonify([record.json() for record in allRecords])

        
    return jsonify(
        {
            "code": 404,
            "message": "There are no records."
        }
    ), 404
   
@app.route("/hotel/<int:booking_id>")
def find_by_user(booking_id):
    r = Hotel_booking.query.filter_by(booking_id=booking_id).first()

    if r:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "username": r.username,
                    "hotel": r.hotel,
                    "city": r.city,
                    "checkin": r.checkin,
                    "checkout": r.checkout
                }
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
    r = Hotel_booking.query.filter_by(booking_id=booking_id).all()
    if r:
        return jsonify(
            {
                "code": 400,
                "message": "Record already exists for this user. Use PUT method if you are trying to update the record."
            }
        ), 400

    data = request.get_json()
    record = Hotel_booking(booking_id, **data)

    try:
        db.session.add(record)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "booking_id": booking_id
                },
                "message": "An error occurred creating the record."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": record.json()
        }
    ), 201

@app.route("/hotel/<int:booking_id>", methods=['PUT'])
def update_record(booking_id):
    r = Hotel_booking.query.filter_by(booking_id=booking_id).first()
    if not r:
        return jsonify(
            {
                "code": 400,
                "message": "Record does not exist for this user. Use POST to create a new record."
            }
        ), 400

    data = request.get_json()
    r.username = data.get('username', r.username)
    r.hotel = data.get('hotel', r.hotel)
    r.city = data.get('city', r.city)
    r.checkin = data.get('checkin', r.checkin)
    r.checkout = data.get('checkout', r.checkout)

    try:
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "booking_id": booking_id
                },
                "message": "An error occurred updating the record."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": r.json()
        }
    ), 201


@app.route("/route/<int:booking_id>", methods=['DELETE'])
def delete_record(booking_id):
    r = Hotel_booking.query.filter_by(booking_id=booking_id).first()
    if not r:
        return jsonify(
            {
                "code": 400,
                "message": "Record does not exist for this user."
            }
        ), 400

    try:
        db.session.delete(r)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "booking_id": booking_id
                },
                "message": "An error occurred deleting the record."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": r.json(),
            "message": "Deleted successfully!"
        }
    ), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

if __name__ == "__main__":
    app.run()
        
