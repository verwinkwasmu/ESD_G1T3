#! /usr/bin/env python3.6

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""
import os
from flask import Flask, jsonify, request

import stripe
# This is your real test secret API key.
stripe.api_key = 'sk_test_51HeLb7GWjRGxBOOYruap689xNCFhMWetmp25MiJz4LGZoJPqSLTCsNhhoqtvt6DW6qKRHf7iiyyZMeRbN61lL6A500O0PzD1vM'

app = Flask(__name__)

@app.route('/make_payment', methods=['POST'])
def create_charge():
    payment_details = request.get_json()
    try:
        # `source` is obtained with Stripe.js; see https://stripe.com/docs/payments/accept-a-payment-charges#web-create-token
        checkout = stripe.checkout.Session.create(
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
            payment_method_types=["card"],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': payment_details['amount'],
                        'product_data': {
                            'name': 'Hotel Dream',
                            'images': ['https://www.swissotel.com/assets/0/92/3686/3768/3770/6442451433/ae87da19-9f23-450a-8927-6f4c700aa104.jpg'],
                        },
                    },
                    'quantity': 1,
                }
            ],
            mode="payment",
        )

        if checkout['payment_status'] == True:
            return jsonify(
                {
                    "code": 200,
                    "status": 'Payment successfully made'
                }
            )
        return jsonify(
            {
                "code": 404,
                "message": "Payment failed"
            }
        ), 404
    except Exception as e:
        return jsonify(error=str(e)), 403

if __name__ == '__main__':
    app.run(port=4242, debug = True)
