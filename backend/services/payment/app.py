from flask import Flask, jsonify, request, send_from_directory
import stripe
from pymongo import MongoClient
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
mongo_client = MongoClient('mongodb+srv://ryanlee99324:BrImAqgUaXaNuEz6@esdproj.r2bp9gh.mongodb.net/') 
db = mongo_client['payment_db']  
payments_collection = db['payments']  

# Set your secret key here
stripe.api_key = 'sk_test_51Op0OtL12QL7JE0ghziI2xjPzuEigrx7p8PJn7HhSF5dUiBf6gJGoeL4olTe5IKswoesxuuJfLMAKhzx5yNOi7AE00LMZM7S4M'

@app.route('/')
def serve_payment_form():
    return jsonify({"code": 200, "message": "HEllo."}), 200

@app.route('/create_payment_intent', methods=['POST'])
def create_payment_intent():
    data = request.json
    print(data)
    try:
        intent = stripe.PaymentIntent.create(
            amount=data.get('amount'),  # Amount in cents
            currency=data.get('currency', 'sgd'),  # Default to USD
            
        )
        payments_collection.insert_one({
            'payment_intent_id': intent.id,
            'amount': data['amount'],
            'currency': data.get('currency', 'sgd'),
            'status': 'created'
        })
        print(intent)
        return jsonify({'clientSecret': intent.client_secret, 'paymentIntent_id': intent.id}), 200
    except stripe.error.StripeError as e:
        print(e)
        return jsonify(error=str(e)), 400

@app.route('/refund', methods=['POST'])
def refund_payment():
    data = request.json
    print(data)
    payment_intent_id = data.get('payment_intent_id')
    amount = data.get('amount') 

    try:
        if amount:
            refund = stripe.Refund.create(
                payment_intent=payment_intent_id,
                amount=amount,
            )
        else:
            refund = stripe.Refund.create(
                payment_intent=payment_intent_id,
            )
        return jsonify(refund), 200
    except Exception as e:
        return jsonify(error=str(e)), 400

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5020)
