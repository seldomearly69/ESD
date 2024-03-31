import bcrypt
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime
from flask_cors import CORS
import json
from flasgger import Swagger

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['MONGO_URI'] = 'mongodb+srv://ryanlee99324:BrImAqgUaXaNuEz6@esdproj.r2bp9gh.mongodb.net/Users'
mongo = PyMongo(app).db.users
app.config['SWAGGER'] = {
    'title': 'User API',
    'uiversion': 3,
    'description':"Allows login and register requests"
}
swagger = Swagger(app)
    
@app.route("/register", methods=["POST"])
def register_user():
    """
    Register a new user
    ---
    tags:
      - Users
    description: Registers a new user with email and password.
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: user@example.com
            password:
              type: string
              example: yourpassword
    responses:
      201:
        description: User registered successfully
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 201
            data:
              type: object
              properties:
                email:
                  type: string
                  example: user@example.com
      400:
        description: Email already has an existing account
    """
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
    data["usertype"] = "customer"
    mongo.insert_one(data)
    return jsonify(
        {
            "code": 201,
            "data": data_dup
            
        }
            ), 201


@app.route("/login", methods=["POST"])
def login():
    """
    User login
    ---
    tags:
      - Users
    description: Logs in a user using email and password.
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: user@example.com
            password:
              type: string
              example: yourpassword
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 200
            data:
              type: object
              properties:
                email:
                  type: string
                  example: user@example.com
                usertype:
                  type: string
                  example: customer
      404:
        description: User does not exist
      400:
        description: Password incorrect
    """
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
                "usertype": result["usertype"]
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
    