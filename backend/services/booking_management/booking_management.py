from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

import time
import sys

app = Flask(__name__)
CORS(app)



@app.route("/search")
def search():
    data = request.get_json()
    fresponse = None
    hresponse = None
    if "flight" in data:
        fresponse = requests.get("http://flight_search:5007/flights", json = data["flight"])
        if (fresponse.status_code == 200):
            fresponse = fresponse.json()

    if "hotel" in data:
        hresponse = requests.get("http://hotel_search:5003/hotels", json = data["hotel"])
        if (hresponse.status_code == 200):
            hresponse = hresponse.json()

    return jsonify({"flight": fresponse, "hotel": hresponse})

@app.route("/book")
def make_booking():
    data = request.get_json()
    flight = data.get("flight", None)
    hotel = data.get("hotel", None)
    amount = 0
    if flight:
        amount += flight["price"]
    if hotel:
        amount += hotel["price"]
    # TO-DO:
    #     Send amount for payment
    #     Send flight booking to database
    #     Send hotel booking to database
    #     Send out email confirmation
    return

    
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008, debug=True)