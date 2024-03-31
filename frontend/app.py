from flask import Flask,render_template
from flask_cors import CORS

app=Flask(__name__)
CORS(app,resources={r"/*": {"origins": "*"}})

@app.route("/login")
def login():
    return render_template("auth/login.html")

@app.route("/register")
def register():
    return render_template("auth/register.html")

@app.route("/booking")
def booking():
    return render_template("booking/booking.html")

@app.route("/flight_search")
def flight_search():
    return render_template("flight_search/flight.html")

@app.route("/hotel_info")
def hotel_info():
    return render_template("hotel_info/info.html")

@app.route("/hotel_management")
def hotel_management():
    return render_template("hotel_management/hotel.html")

@app.route("/hotel_search")
def hotel_search():
    return render_template("hotel_search/hotel.html")

@app.route("/home")
def home():
    return render_template("nav/home.html")

@app.route("/hotel")
def hotel():
    return render_template("nav/hotel.html")

@app.route("/flight")
def flight():
    return render_template("nav/flight.html")

@app.route("/route_planning")
def route_planning():
    return render_template("route_planning/route_planning.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5050, debug=True)
    