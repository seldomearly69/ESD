from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/Hotel'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

# app.config['SWAGGER'] = {
#  'title': 'Book microservice API',
#  'version': 1.0,
#  "openapi": "3.0.2",
#  'description': 'Allows create, retrieve, update, and delete of books'
# }

# swagger = Swagger(app)

class Hotel(db.Model):
    __tablename__ = 'Hotel'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    username = db.Column(db.String(80), nullable=False)
    hotel = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    checkin = db.Column(Date, nullable=False)
    checkout = db.Column(Date, nullable=False)
    


    def __init__(self, username, hotel, city, checkin, checkout):
        self.username = username
        self.hotel = hotel
        self.city = city
        self.checkin = checkin
        self.checkout = checkout
        
    def json(self):
        return {"username": self.username, "hotel": self.hotel, "city": self.city, "checkin": self.checkin, "checkout":self.checkout}


@app.route("/bookings/<string:userName>")
def find_bookings_by_username(userName):
    
    bookings = db.session.query(Hotel).filter_by(username=userName).all()


    if bookings:
        bookings_data = [booking.json() for booking in bookings]
        return jsonify(
            {
                "code": 200,
                "data": bookings_data
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Bookings not found."
        }
    ), 404



@app.route("/bookings/", methods=['POST'])
def create_hotelBooking():
    data = request.get_json()
    
    if (db.session.scalars(
    	db.select(Hotel).filter_by(username=data["username"], hotel=data["hotel"], city=data["city"], checkin=data["checkin"], checkout=data["checkout"]).
    	limit(1)
    ).first()
    ):
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "booking": data
                    },
                    "message": "Booking already exists."
                }
            ), 400
            
    hotelBooking = Hotel(**data)


    try:
        db.session.add(hotelBooking)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "username": data["username"]
                },
                "message": "An error occurred creating the hotel booking."
            }
        ), 500


    return jsonify(
        {
            "code": 201,
            "data": hotelBooking.json()
        }
    ), 201

@app.route("/bookings/", methods=['DELETE'])
def delete_bookings():
    data = request.get_json()
    
    cityName = data["city"]
    hotelName = data["hotel"]
    
    bookings = Hotel.query.filter_by(city=cityName, hotel=hotelName).all()
    
    if bookings:
        for booking in bookings:
            db.session.delete(booking)
            
        db.session.commit()
        return jsonify({"message": "Bookings deleted successfully."}), 200
    else:
        return jsonify({"message": "No matching bookings found."}), 404

        
if __name__ == '__main__':
    app.run(port=5001, debug=True)