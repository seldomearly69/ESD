from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import pika


app = Flask(__name__)
CORS(app)

@app.route("/delete_bookings", methods=["POST"])
def delete_booking():
    data = request.get_json()
    delete_response = requests.delete("http://hotel_booking:5009/bookings/", json = data["flight"])
    if delete_response.status_code == 200:
        print("delete operation was done...")
        deleted_bookings = delete_response["deleted_bookings"]
        for booking in deleted_bookings:
            print("sending email to inform user that their booking has been deleted...")
            # TO-DO--> send the deleted booking as message to amqp broker, broker passes to 
            # email microservice when it comes online???
    else:
        return jsonify({"message": delete_response["message"]})
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)
