from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import mysql.connector
import time
import bcrypt

app = Flask(__name__)
# connect to DB
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("dbURL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash =password_hash
        
    def __repr__(self):
        return f'<User: {self.username}>'
    
    def json(self):
        return {"username": self.username, "password": self.password_hash}
        
def connect_to_db_with_retry():
    max_retries = 20
    retries = 0

    while retries < max_retries:
        try:
            # Attempt to connect to the database
            connection = mysql.connector.connect(
                host= 'mysql',
                user='sample',
                password='password',
                database='mydb'
            )

            print("Connected to the database!")
            return connection

        except mysql.connector.Error as e:
            print(f"Failed to connect to the database: {e}")
            retries += 1
            print(f"Retrying... Attempt {retries}/{max_retries}")
            time.sleep(5)  # Wait for 5 seconds before the next attempt

    print("Max retries reached. Could not connect to the database.")
    return None

connection = connect_to_db_with_retry()


@app.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    print(data)
    if (db.session.scalars(
    	db.select(User).filter_by(username=data["username"]).
    	limit(1)
    ).first()
    ):
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "userId": data["username"]
                    },
                    "message": "User already registers."
                }
            ), 400

    encoded_password = data["password_hash"].encode('utf-8')
    data["password_hash"] = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
    newUser = User(**data)
    
    try:
        db.session.add(newUser)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "userId": data["username"]
                },
                "message": "An error occurred registering the user."
            }
        ), 500


    return jsonify(
        {
            "code": 201,
            "data": newUser.json()
        }
    ), 201


@app.route("/login", methods=["POST"])
def login():
    print("logging in...")
    data = request.get_json()
    print(data)
    user = db.session.scalars(
    	db.select(User).filter_by(username=data["username"]).
    	limit(1)
    ).first()
    if (user):
        encoded_password = data["password_hash"].encode('utf-8')
        stored_password_hash = user.password_hash.encode('utf-8')
        password_match = bcrypt.checkpw(encoded_password, stored_password_hash)
        if(password_match):
            return jsonify({
                "code": 200,
                "data": {
                    "userId": data["username"],
                    # supposed to return api-key-auth to front-end??
                    "api-key-auth": "admin/user"
                }
            }), 200
        else:
            return jsonify(
            {
                "code": 400,
                "data": {
                    "userId": data["username"]
                },
                "message": "Username or password incorrect!"
            }
        ), 400
    else:
        return jsonify(
            {
                "code": 400,
                "data": {
                    "userId": data["username"]
                },
                "message": "Username or password incorrect!"
            }
        ), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)
    