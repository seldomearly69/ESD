import bcrypt
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

app.config['MONGO_URI'] = 'mongodb+srv://ryanlee99324:BrImAqgUaXaNuEz6@esdproj.r2bp9gh.mongodb.net/Users'
mongo = PyMongo(app).db.users

    
@app.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    data_dup = data.copy()

    if mongo.find_one({"email": data["email"]}):
        return jsonify(
            {
                "code": 400,
                "message": "Email already has an existing account"
            }
        ), 400
    encoded_password = data["password"].encode('utf-8')
    data["password"] = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
    mongo.insert_one(data)
    return jsonify(
        {
            "code": 201,
            "data": data_dup
        }
            ), 201


@app.route("/login", methods=["POST"])
def login():
    print("logging in...")
    data = request.get_json()
    result = mongo.find_one({"email": data["email"]})
    if not result:
        return jsonify({
                "code": 404,
                "message": "User does not exist"
            }), 404
    
    encoded_password = data["password"].encode('utf-8')
    password_match = bcrypt.checkpw(encoded_password, result["password"])
    if(password_match):
        return jsonify({
            "code": 200,
            "data": {
                "email": data["email"],
                }
            }), 200
    else:
        return jsonify(
        {
            "code": 400,
            "message": "Password incorrect!"
        }
    ), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5002, debug=True)
    