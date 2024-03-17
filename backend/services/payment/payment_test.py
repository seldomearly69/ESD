# payment.py
from flask import Flask, jsonify, request
import stripe

app = Flask(__name__)

# Set your Stripe API key here
stripe.api_key = 'sk_test_51Op0OtL12QL7JE0ghziI2xjPzuEigrx7p8PJn7HhSF5dUiBf6gJGoeL4olTe5IKswoesxuuJfLMAKhzx5yNOi7AE00LMZM7S4M'

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
        return jsonify({'clientSecret': intent.client_secret}), 200
    except Exception as e:
        return jsonify(error=str(e)), 400

@app.route('/process_payment', methods=['POST'])
def process_payment():
    token = request.form.get('stripeToken')
    amount = request.form.get('amount')
    currency = request.form.get('currency')

    try:
        # Use the token, amount, and currency to process the payment
        # Call Stripe API to charge the payment
        payment = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Amount in cents
            currency=currency,
            payment_method_types=['card'],
            payment_method=token,
            confirm=True,  # Confirm the payment immediately
        )

        # Check if the payment was successful
        if payment.status == 'succeeded':
            # Payment was successful
            return jsonify({'paymentStatus': 'succeeded'}), 200
        else:
            # Payment failed
            return jsonify({'paymentStatus': 'failed'}), 400

    except stripe.error.StripeError as e:
        # Handle Stripe errors
        return jsonify({'error': str(e)}), 400

    except Exception as e:
        # Handle other exceptions
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return open('payment.html').read()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
