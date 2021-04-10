from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http

import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

# booking_URL = environ.get('booking_URL') or "https://esdg1t3-booking.herokuapp.com/booking"
# cart_URL = os.environ.get("cart_URL") or "https://esdg1t3-cart.herokuapp.com/cart"
# facility_URL = environ.get('facility_URL') or "https://esdg1t3-facility.herokuapp.com/facility"

booking_URL = "http://13.213.13.210:5000/booking"
cart_URL = "http://18.141.190.114:5001/cart"
facility_URL = "http://54.255.129.160:5002/facility"


@app.route("/book_facilities/send_hotel_facilities", methods=['POST'])
def send_facilities_booking():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            booking_details = request.get_json()
            print("\nReceived a request to order facilities in JSON:", booking_details)

            # do the actual work
            # 1. Get all cart purchases using booking_id
            result = send_hotel_facilities(booking_details)
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

def send_hotel_facilities(booking_details):

    item_name = booking_details['item_name']
    guest_name = booking_details['name']
    booking_id = booking_details['booking_id']
    email = booking_details['email']
    item_id = booking_details['item_id']
    order_datetime = booking_details['order_datetime'][:10] + " " + booking_details['order_datetime'][11:19]

    f_order = {
        "item_id": item_id,
        "order_datetime": order_datetime
    }

    add_fb_result = invoke_http(cart_URL + "/add_fb/" + booking_id, method='POST', json=f_order)
    if add_fb_result['code'] not in range(200, 300):
        return {
            'code': 404,
            'status': 'failed to add facility booking'
        }
    
    print("add_fb_result", add_fb_result)

    email_details = {
        "email": email,
        "guest_name": guest_name,
        "quantity": add_fb_result["data"]['rs_quantity'],
        "price": add_fb_result["data"]['price'],
        "item_name" : item_name,
        "date_time": add_fb_result["data"]["order_datetime"],
        "order_id": add_fb_result["data"]["order_id"],
        "booking_id": add_fb_result["data"]["booking_id"],
        "type": "facility"
    }

    print('email_details:', email_details)
    message = json.dumps(email_details)

    amqp_setup.check_setup()

    print('\n\n-----Publishing the (facility notification) message with routing_key=facility.notification-----')

    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="facility.notification",
                                        body=message, properties=pika.BasicProperties(delivery_mode=2))
    # make message persistent within the matching queues until it is received by some receiver
    # (the matching queues have to exist and be durable and bound to the exchange)

    # - reply from the invocation is not used;
    # continue even if this invocation fails
    print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(
        add_fb_result['code']), message)

    return {
        "code": 201,
        "booking_result": {
            "email": email,
            "guest_name": guest_name,
            "status": "success"
        }
    }
    
# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for book facilities...")
    port = 5300 or int(os.environ.get('PORT', 5300))
    app.run(host="0.0.0.0", port=port, debug=False)
