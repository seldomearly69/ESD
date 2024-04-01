from flask import Flask, jsonify, request, send_from_directory
import stripe
from flasgger import Swagger
from pymongo import MongoClient
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
mongo_client = MongoClient('mongodb+srv://ryanlee99324:BrImAqgUaXaNuEz6@esdproj.r2bp9gh.mongodb.net/') 
db = mongo_client['payment_db']  
payments_collection = db['payments']  
app.config['SWAGGER'] = {
    'title': 'Payment API',
    'uiversion': 3,
    'description':"Allows refund and payment intent requests"
}
swagger = Swagger(app)
# Set your secret key here
stripe.api_key = 'sk_test_51Op0OtL12QL7JE0ghziI2xjPzuEigrx7p8PJn7HhSF5dUiBf6gJGoeL4olTe5IKswoesxuuJfLMAKhzx5yNOi7AE00LMZM7S4M'

@app.route('/')
def serve_payment_form():
    return jsonify({"code": 200, "message": "HEllo."}), 200

@app.route('/create_payment_intent', methods=['POST'])
def create_payment_intent():
    """
    Create a new payment intent
    ---
    tags:
      - Payments
    description: Creates a new payment intent to process a payment.
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Payment intent details
        required: true
        schema:
          type: object
          required:
            - amount
          properties:
            amount:
              type: integer
              description: The amount to charge in the smallest currency unit (e.g., cents for USD)
            currency:
              type: string
              default: "sgd"
              description: The currency of the payment
    responses:
      200:
        description: Payment intent created successfully
        schema:
          type: object
          properties:
            clientSecret:
              type: string
              description: The client secret of the payment intent
      400:
        description: Error creating the payment intent
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
    """
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
    """
    Process a payment refund
    ---
    tags:
      - Payments
    description: Refunds a payment based on the payment intent ID and optionally a specific amount.
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Refund details
        required: true
        schema:
          type: object
          properties:
            payment_intent_id:
              type: string
              description: The ID of the payment intent to refund
            amount:
              type: integer
              description: Optional amount to refund in the smallest currency unit (e.g., cents for USD)
    responses:
      200:
        description: Refund processed successfully
        schema:
          type: object
          properties:
            id:
              type: string
              description: The ID of the refund
            status:
              type: string
              description: The status of the refund
      400:
        description: Error processing the refund
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
    """
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
            payments_collection.insert_one({
            'payment_intent_id': payment_intent_id,
            'amount': data['amount'],
            'currency': data.get('currency', 'sgd'),
            'status': 'refunded'
        })
        else:
            refund = stripe.Refund.create(
                payment_intent=payment_intent_id,
            )
        return jsonify(refund), 200
    except Exception as e:
        return jsonify(error=str(e)), 400

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5020)
