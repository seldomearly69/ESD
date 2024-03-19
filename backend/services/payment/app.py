from flask import Flask, jsonify, request, send_from_directory
import stripe

app = Flask(__name__, static_url_path='', static_folder='.')

# Set your secret key here
stripe.api_key = 'sk_test_51Op0OtL12QL7JE0ghziI2xjPzuEigrx7p8PJn7HhSF5dUiBf6gJGoeL4olTe5IKswoesxuuJfLMAKhzx5yNOi7AE00LMZM7S4M'

@app.route('/')
def serve_payment_form():
    return send_from_directory('.', 'stripe.html')

@app.route('/create_payment_intent', methods=['POST'])
def create_payment_intent():
    data = request.json
    try:
        intent = stripe.PaymentIntent.create(
            amount=data['amount'],  # Amount in cents
            currency=data.get('currency', 'usd'),  # Default to USD
            
        )
        print(intent)
        return jsonify({'clientSecret': intent.client_secret}), 200
    except Exception as e:
        return jsonify(error=str(e)), 400

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
