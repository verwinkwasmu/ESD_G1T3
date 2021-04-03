from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os, sys
from os import environ
import stripe
import requests
from invokes import invoke_http
import pika

app = Flask(__name__)
CORS(app)

booking_URL = "http://localhost:5000/booking"
cart_URL = "http://localhost:5001/cart"
payment_URL = "http://localhost:4242/create-checkout-session"


@app.route("/calc_total", methods=['POST'])
def calc_total_payment():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            booking_id = request.get_json()
            print("\nReceived a request to get total payment amount in JSON:", booking_id)
            # do the actual work
            # 1. Get total amount using booking_id
            result = total_amount(request.json.get('booking_id'))
            return jsonify(result), 200

        except Exception as e:
            return jsonify({
                "code": 404,
                "message": str(e)
            }), 404

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data()),
        "test": str(request.is_json)
    }), 400


def total_amount(booking_id):
    # 2. Send booking id to booking microservice to retrieve all booking items
    # Invoke booking microservice
    print('\n-----Invoking booking microservice-----')
    booking_result = invoke_http(booking_URL + "/" + str(booking_id))
    print('booking_result:', booking_result)

    code = booking_result["code"]
    if code not in range(200, 300):
        # if there are no bookings, return message
        return {
            "code": 404,
            "data": {"booking_result": booking_result}
        }

    room_price = booking_result['data']['room_price']
    discount = booking_result['data']['discount']
    print(discount)
    # 3. get all facilities and room services from cart microservice
    print('\n-----Invoking cart microservice-----')

    cart_items = invoke_http(cart_URL + "/booking/" + booking_id)
    cart_items = cart_items['data']['bookings']
    if len(cart_items):
        total = 0
        for purchase in cart_items:
            if purchase['price'] != None:
                total += float(purchase['price']) * \
                    int(purchase['rs_quantity'])

    total = round((total + room_price) * (1 - discount), 2)

    return {
        "code": 200,
        "total": total
    }


@app.route("/process_payment", methods=['POST'])
def process_payment():
    if request.is_json:
        try:
            print("\nReceived composite POST request from HTML:",
                  request.get_json())
            # do the actual work
            # 1. Send to payment microservice
            result = invoke_http(payment_URL, method='POST', json=request.get_json())
            return jsonify(result)

        except Exception as e:
            return jsonify({
                "code": 404,
                "message": str(e)
            }), 404

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data()),
        "test": str(request.is_json)
    }), 400




# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for procesing checkouts...")
    app.run(host="0.0.0.0", port=5400, debug=True)
