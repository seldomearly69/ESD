from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://ryanlee99324:BrImAqgUaXaNuEz6@esdproj.r2bp9gh.mongodb.net/routes'
# Initialize flasgger 
app.config['SWAGGER'] = {
    'title': 'Route Saver API',
    'version': 1.0,
    "openapi": "3.0.2",
    'description': 'Allows retrieval and update of saved routes'
}
swagger = Swagger(app)

mongo = PyMongo(app)
CORS(app, resources={r"/*": {"origins": "*"}})


#Find Bookings by email
@app.route("/routes/get/<string:email>")
def find_booking(email):
    """
    Gets the saved routes of the user
    ---
    parameters:
    -   in: path
        name: email
        required: true
    responses:
        200:
            description: Successful retrieval
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            code:
                                type: integer
                                example: 200
                            data:
                                type: object
                                additionalProperties:
                                    type: array
                                    items:
                                        type: string
                                example:
                                    "Singapore Tour": 
                                        - "Marina bay"
                                        - "singapore zoo"
                                        - "resort world sentosa"
                                        - "chinatown mrt"
                                    "Singapore March Tour":
                                        - "gardens by the bay"
                                        - "indian heritage centre"
                                        - "marina bay sands"
                                        - "pearl's hill city park"
        404:
            description: Record not found
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            code:
                                type: integer
                                example: 404
                            message:
                                type: string
                                example: "Record not found."
    """
    print(mongo, flush=True)
    r = mongo.db.routes.find_one({"email": email})
    
    if r:
        del r["_id"]
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



#Save Routes
@app.route("/routes/save/<string:email>", methods=['PUT'])
def save_routes(email):
    """
    Updates routes associated with a specific email.
    ---
    parameters:
    -   in: path
        name: email
        required: true
        description: Email address to save routes for.
        schema:
            type: string
    requestBody:
        required: true
        content:
            application/json:
                schema:
                    type: object
                    properties:
                        routes:
                            type: object
                            additionalProperties:
                                type: array
                                items:
                                    type: string
    responses:
        '200':
            description: Successful save
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            message:
                                type: string
                                example: "Saved successfully"
        '500':
            description: Internal Server Error
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            error:
                                type: string
                                example: "Internal Server Error"
    """
    data = request.get_json()
    result = mongo.db.routes.update_one({"email": email}, {"$set": {"routes": data}}, upsert = True)
    if result.modified_count > 0:
        return jsonify(data), 200
    else:
        return jsonify("No records updated"),200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
