##################################################################################################################################
#
#   Endpoints:
#   - GET "/all_routes" 
#       -> returns all records in database
#
#   - GET "/route" 
#       -> takes in 1 request parameter [uid] of user whose record to be retrieved
#       -> E.g. "/route/1" retrieves record of user with uid == 1
#
#   - POST "/route"
#       -> takes in 1 request parameter [uid] to create record with
#       -> request body JSON requires 2 properties [lats], [longs] which are ordered arrays of pairing lats and longs
#       -> E.g. "/route/1" creates record of user with uid == 1
#
#   - PUT "/route"
#       -> takes in 1 request parameter [uid] of user whose record to be updated
#       -> request body JSON requires UP TO 2 properties [lats], [longs] which are ordered arrays of pairing lats and longs
#       -> E.g. "/route/1" udpate record of user with uid == 1
#
#   - DELETE "/route"
#       -> takes in 1 request parameter [uid] of user whose record to be deleted
#       -> E.g. "/route/1" deletes record of user with uid == 1
#
##################################################################################################################################

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import psycopg2
import time
import sys

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://is213:8CRjw8442oS@route_records_db:5432/is213'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def wait_for_db():
    max_retries = 30
    retries = 0

    while retries < max_retries:
        try:
            conn = psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI'])
            conn.close()
            print("Database is reachable.")
            return
        except psycopg2.OperationalError as e:
            print(f"Database not ready yet. Retrying... ({retries}/{max_retries})")
            retries += 1
            time.sleep(1)

    print("Failed to connect to the database after retries. Exiting.")
    sys.exit(1)

wait_for_db()


class RouteRecord(db.Model):
    __tablename__ = 'route_record'

    uid = db.Column(db.Integer, primary_key=True)
    lats = db.Column(db.JSON, nullable=False)
    longs= db.Column(db.JSON, nullable=False)

    def __init__(self, uid, lats, longs):
        self.uid = uid
        self.lats = lats
        self.longs = longs

    def json(self):
        return {"uid": self.uid, "lats": self.lats, "longs": self.longs}

@app.route("/all_routes")
def get_all():
    allRecords = RouteRecord.query.all()

    if len(allRecords):
        return jsonify([record.json() for record in allRecords])

        
    return jsonify(
        {
            "code": 404,
            "message": "There are no records."
        }
    ), 404
   
@app.route("/route/<int:uid>")
def find_by_user(uid):
    r = RouteRecord.query.filter_by(uid=uid).first()

    if r:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "lats": r.lats,
                    "longs": r.longs
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Record not found."
        }
    ), 404

@app.route("/route/<int:uid>", methods=['POST'])
def create_record(uid):
    r = RouteRecord.query.filter_by(uid=uid).all()
    if r:
        return jsonify(
            {
                "code": 400,
                "message": "Record already exists for this user. Use PUT method if you are trying to update the record."
            }
        ), 400

    data = request.get_json()
    record = RouteRecord(uid, **data)

    try:
        db.session.add(record)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "uid": uid
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

@app.route("/route/<int:uid>", methods=['PUT'])
def update_record(uid):
    r = RouteRecord.query.filter_by(uid=uid).first()
    if not r:
        return jsonify(
            {
                "code": 400,
                "message": "Record does not exist for this user. Use POST to create a new record."
            }
        ), 400

    data = request.get_json()
    r.lats = data.get('lats', r.lats)
    r.longs = data.get('longs', r.longs)

    try:
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "uid": uid
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


@app.route("/route/<int:uid>", methods=['DELETE'])
def delete_record(uid):
    r = RouteRecord.query.filter_by(uid=uid).first()
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
                    "uid": uid
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
    app.run(host='0.0.0.0', port=5001, debug=True)