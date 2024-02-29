from flask import Flask, jsonify, request
import stripe

app = Flask(__name__)

stripe.api_key = ''

@app.route('/create_payment', methods=['POST'])
def create_payment():
    data = request.json
    amount = data.get('amount')
    currency = data.get('currency', 'usd')  # Default to USD if not provided

    try:
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Amount in cents
            currency=currency,
            metadata={'integration_check': 'accept_a_payment'},
        )
        return jsonify({'clientSecret': intent['client_secret']}), 200
    except Exception as e:
        return jsonify(error=str(e)), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
