from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://ryanlee99324:BrImAqgUaXaNuEz6@esdproj.r2bp9gh.mongodb.net/'
mongo = PyMongo(app).db.Users


class Hotel:
    @staticmethod
    def json(booking):
        return {
            "rid": booking["rid"],
            "username": booking["username"],
            "lats": booking["lats"],
            "longs": booking["longs"]
        }
    
#Get all routes
@app.route("/all_routes")
def get_all():
    allRecords = mongo.db.routes.find()

    if allRecords.count():
        return jsonify([record for record in allRecords])

    return jsonify(
        {
            "code": 404,
            "message": "There are no records."
        }
    ), 404

#Find Booking
@app.route("/routes/<int:rid>")
def find_booking(rid):
    r = mongo.db.routes.find_one({"rid": rid})
    if r:
        return jsonify(
            {
                "code": 200, 
                "data": r
            }
        )
    return jsonify(
        {
            "code": 404, 
            "message": "Record not found."
        }
    ), 404


#Create Record
@app.route("/routes/<int:rid>", methods=['POST'])
def create_record(rid):
    r = mongo.db.routes.find_one({"rid": rid})
    if r:
        return jsonify({"code": 400, "message": "Record already exists for this user. Use PUT method if you are trying to update the record."}), 400

    data = request.get_json()
    data['rid'] = rid
    mongo.db.routes.insert_one(data)
    return jsonify(
        {
            "code": 201, 
            "data": data
        }
    ), 201


#Update Record
@app.route("/routes/<int:rid>", methods=['PUT'])
def update_record(rid):
    r = mongo.db.routes.find_one(
        {
            "rid": rid
        }
        )
    if not r:
        return jsonify(
            {
                "code": 400, 
                "message": "Record does not exist for this user. Use POST to create a new record."
            }
            ), 400

    data = request.get_json()
    mongo.db.routes.update_one({"rid": rid}, {"$set": data})
    return jsonify(
        {
            "code": 201, 
            "data": r
        }
    ), 201



#Delete Record
@app.route("/routes/<int:rid>", methods=['DELETE'])
def delete_record(rid):
    r = mongo.db.routes.find_one({"rid": rid})
    if not r:
        return jsonify(
            {
                "code": 400, 
                "message": "Record does not exist for this user."
            }
        ), 400

    mongo.db.routes.delete_one({"rid": rid})
    return jsonify(
        {
            "code": 201, 
            "data": r, "message": "Deleted successfully!"
        }
    ), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5011, debug=True)
