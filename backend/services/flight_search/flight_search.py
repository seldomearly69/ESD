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


@app.route("/flights", methods=["POST"])
def search():
    
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