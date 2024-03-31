from flask import Flask, request, jsonify
from flask_cors import CORS
from flasgger import Swagger
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import ObjectId

from serpapi import GoogleSearch

import time
import sys

app = Flask(__name__)
CORS(app)


app.config['SWAGGER'] = {
    'title': 'Flight Search API',
    'uiversion': 3,
    'description':"Allows post request for flight search"
}
swagger = Swagger(app)

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


@app.route("/flights", methods=["POST"])
def search():
    """
    Search for flights based on given parameters
    ---
    tags:
      - Flights
    description: Search for flights using various search parameters.
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: header
        name: SERPAPI-KEY
        type: string
        required: true
        description: API key required to authorize the request
      - in: body
        name: body
        description: Flight search parameters including the user's email
        required: true
        schema:
          type: object
          required:
            - email
          properties:
            email:
              type: string
              description: Email address of the user performing the search
            departure_airport:
              type: string
              description: IATA code of the departure airport
            arrival_airport:
              type: string
              description: IATA code of the arrival airport
            departure_date:
              type: string
              format: date
              description: Departure date in YYYY-MM-DD format
            return_date:
              type: string
              format: date
              description: Return date in YYYY-MM-DD format
            adults:
              type: integer
              description: Number of adults
            children:
              type: integer
              description: Number of children
            infants:
              type: integer
              description: Number of infants
            travel_class:
              type: string
              description: Travel class (e.g., economy, business)
    responses:
      200:
        description: An array of search results matching the criteria
      400:
        description: Invalid input parameters
    definitions:
      FlightResult:
        type: object
        properties:
          airline:
            type: string
            description: Name of the airline
          flight_number:
            type: string
            description: Flight number
          departure_airport:
            type: string
            description: Departure airport IATA code
          arrival_airport:
            type: string
            description: Arrival airport IATA code
          departure_time:
            type: string
            format: datetime
            description: Departure time
          arrival_time:
            type: string
            format: datetime
            description: Arrival time
          price:
            type: number
            format: float
            description: Price of the flight
    """
    data = request.get_json()
    print(data,flush=True)

    coll = db[data["email"]]
    
    temp = data
    temp["output"] = "json"
    temp["source"] = "python"
    result = coll.find_one({"searchParams": temp})
    print(result, flush=True)
    if result:
        print("hi", flush=True)
        return result["cachedResult"]

    search = GoogleSearch(data)
    results = search.get_dict()

    result = coll.insert_one({"searchParams": data, "cachedResult": results})
    return jsonify(results)
    
    
@app.route("/drop")
def drop_cache():
    coll = db[request.get_json()["email"]]
    coll.drop()
    return "success"






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007, debug=True)