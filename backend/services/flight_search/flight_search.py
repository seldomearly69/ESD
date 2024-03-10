from flask import Flask, request, jsonify
from flask_cors import CORS

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import ObjectId

from serpapi import GoogleSearch

import time
import sys

app = Flask(__name__)
CORS(app)



def connect_to_db():
    max_retries = 30
    retries = 0

    while retries < max_retries:
        try:
            # Update the MongoDB connection details
            client = MongoClient('mongodb+srv://ryanlee99324:BrImAqgUaXaNuEz6@esdproj.r2bp9gh.mongodb.net/')
            # Try to run a simple command to check if the database is reachable
            client.admin.command('ping')
            print("Database is reachable.")
            return client
        except ConnectionFailure as e:
            print(f"Database not ready yet. Retrying... ({retries}/{max_retries})")
            retries += 1
            time.sleep(1)

    print("Failed to connect to the database after retries. Exiting.")
    sys.exit(1)

client = connect_to_db()
db = client["flightsearches"]
coll = db["flightsearches"]

@app.route("/search")
def search():

    data = request.get_json()
    params = {
    "engine": "google_flights",
    "departure_id": data["departure_id"],
    "arrival_id": data["arrival_id"],
    "outbound_date": data["outbound_date"],
    "return_date": data["return_date"],
    "currency": "SGD",
    "hl": "en",
    "api_key": "f3f6e4266e8a55e158eccff91716b1033839ff2368200bf47edd94ef78e8484b",
    "type": 1,
    "travel_class": data["travel_class"],
    "adults": data["adults"],
    "children": data["children"],
    "max_price": data["max_price"],


    }
    if "departure_key" in data:
        params["departure_key"] = data["departure_key"]
    search = GoogleSearch(params)
    results = search.get_dict()
    return jsonify(results)

    
def search_cache():
    oid = ObjectId("65ec2b7ebb9ea281df58560c")
    result = coll.find_one({"_id": oid})
    print(result, flush=True)
    return

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007, debug=True)