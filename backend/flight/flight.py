from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/flightdb'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
app.app_context().push()

#Flight Bookings Table
class Flight_booking(db.Model):
    booking_id = db.Column("id",db.Integer, primary_key=True)
    username = db.Column("username", db.String(100))
    flight_no = db.Column("flight_no",db.Integer)
    airline = db.Column("airline", db.String(100))
    departure_city = db.Column("departure_city", db.String(100))
    arrival_city = db.Column("arrival_city", db.String(100))
    #datetime(year,month,day,hour,minute,second,microsecond)
    departure = db.Column("departure", db.DateTime)
    arrival = db.Column("arrival", db.DateTime)

    def __init__(self, username, flight_no, airline,departure_city, arrival_city, departure, arrival):
        self.username = username
        self.flight_no = flight_no
        self.airline  = airline
        self.departure_city = departure_city
        self.arrival_city = arrival_city
        self.departure = departure
        self.arrival = arrival

    def json(self):
        return {
            "booking_id": self.booking_id,
            "username": self.username,
            "flight_no": self.flight_no,
            "airline": self.airline,
            "departure_city": self.departure_city,
            "arrival_city": self.arrival_city,
            "departure": self.departure.strftime("%Y-%m-%d %H:%M:%S"),
            "arrival": self.arrival.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def __repr__(self):
        return f'<Username: {self.username}> - <BookingId: {self.booking_id}>'

#Get all records
@app.route("/all_flights")
def get_all():
    allRecords = Flight_booking.query.all()

    if len(allRecords):
        return jsonify([record.json() for record in allRecords])

        
    return jsonify(
        {
            "code": 404,
            "message": "There are no records."
        }
    ), 404

#Find booking by id
@app.route("/flight/<int:booking_id>")
def find_booking(booking_id):
    r = Flight_booking.query.filter_by(booking_id=booking_id).first()

    if r:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "username": r.username,
                    "flight_no": r.flight_no,
                    "airline": r.airline,
                    "departure_city": r.departure_city,
                    "arrival_city": r.arrival_city,
                    "departure": r.departure,
                    "arrival": r.arrival,
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Record not found."
        }
    ), 404

#Create Record
@app.route("/flight/<int:booking_id>", methods=['POST'])
def create_record(booking_id):
    r = Flight_booking.query.filter_by(booking_id=booking_id).all()
    if r:
        return jsonify(
            {
                "code": 400,
                "message": "Record already exists for this user. Use PUT method if you are trying to update the record."
            }
        ), 400

    data = request.get_json()
    record = Flight_booking(**data)

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

#Update Record
@app.route("/flight/<int:booking_id>", methods=['PUT'])
def update_record(booking_id):
    r = Flight_booking.query.filter_by(booking_id=booking_id).first()
    if not r:
        return jsonify(
            {
                "code": 400,
                "message": "Record does not exist for this user. Use POST to create a new record."
            }
        ), 400

    data = request.get_json()
    r.username = data.get('username', r.username)
    r.flight_no = data.get('flight_no', r.flight_no)
    r.airline = data.get('airline', r.airline)
    r.departure_city = data.get('departure_city', r.departure_city)
    r.arrival_city = data.get('arrival_city', r.arrival_city)
    r.departure = data.get('departure', r.departure)
    r.arrival = data.get('arrival', r.arrival)

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

#Delete Record
@app.route("/flight/<int:booking_id>", methods=['DELETE'])
def delete_record(booking_id):
    r = Flight_booking.query.filter_by(booking_id=booking_id).first()
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
    app.run(host='0.0.0.0', port=5002, debug=True)
        
