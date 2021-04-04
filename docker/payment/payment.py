#! /usr/bin/env python3.6

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import stripe
# This is a sample test API key. Sign in to see examples pre-filled with your key.
stripe.api_key = os.environ.get(
    "STRIPE_SK_API_KEY") or 'sk_test_51HeLb7GWjRGxBOOYruap689xNCFhMWetmp25MiJz4LGZoJPqSLTCsNhhoqtvt6DW6qKRHf7iiyyZMeRbN61lL6A500O0PzD1vM'

app = Flask(__name__,
            static_url_path='',
            static_folder='.')
CORS(app)

YOUR_DOMAIN = 'https://esdg1t3ui.herokuapp.com/hotel_UI'

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        value = request.get_json()
        amount = value['amount']
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'sgd',
                        'unit_amount': amount,
                        'product_data': {
                            'name': 'Hotel Dream',
                            'images': ['https://www.swissotel.com/assets/0/92/3686/3768/3770/6442451433/ae87da19-9f23-450a-8927-6f4c700aa104.jpg'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
        return jsonify({'id': checkout_session.id})
    except Exception as e:
        return jsonify(error=str(e)), 403

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 4242)) or 4242
    app.run(host="0.0.0.0",port=port, debug=False)