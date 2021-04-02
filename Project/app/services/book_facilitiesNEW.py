from flask import Flask, request, jsonify
from flask_cors import CORS

import os

import requests
from invokes import invoke_http


app = Flask(__name__)
CORS(app)


booking_URL = "http://localhost:5000/booking"
cart_URL = "http://localhost:5001/cart"
facility_URL = "http://localhost:5002/facility"


@app.route("/book_facilities", methods=["POST"])
def book_facilities():
    if request.is_json:
        try:
            booking_details = request.get_json()
            print("\nReceived a request to order room service in JSON:",
                  booking_details)

            # do the actual work
            # 1. Get all cart purchases using booking_id
            result = get_guest_details(request.json.get(
                'booking_id'))
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


def get_guest_details(booking_id,):
    # 8. Send booking id to booking microservice to booking info (guest_name and email)
    # Invoke booking microservice
    print('\n-----Invoking booking microservice-----')
    booking_result = invoke_http(booking_URL + "/" + booking_id)

    # 9. Return guest details
    guest_details = {
        "email": booking_result['data']['email'],
        "guest_name": booking_result['data']['guest_name']
    }
    print("booking_result:", guest_details)

    code = booking_result["code"]
    if code not in range(200, 300):

        # if there are no bookings, return message
        return {
            "code": 404,
            "data": {"booking_result": booking_result}
        }
    else:
        return {
            "booking_result": booking_result
        }


# get list of facilities and display vacancies
@app.route("/book_facilities/get_available_facilities")
def get_hotel_facility():
    if request.is_json:
        try:
            result = invoke_http(facility_URL)
            facility_name_list = []

            for facility in result['data']['facilities']:
                facility_name = {}
                facility_name['item_desc'] = facility['item_desc']
                facility_name['item_id'] = facility['item_id']
                facility_name['item_name'] = facility['item_name']
                facility_name['item_price'] = facility['item_price']
                facility_name['max_capacity'] = facility['max_capacity']
                facility_name_list.append(facility_name)

            return {
                "code": 200,
                "data": {"facility_deeds": facility_name_list}
            }

        except Exception as e:
            return jsonify({
                "code": 404,
                "message": str(e)
            }), 404


@app.route("/book_facilities/send_hotel_facilities", method=['POST'])
def send_facilities_booking():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            booking_details = request.get_json()
            print("\nReceived a request to order facilities in JSON:", booking_details)

            # do the actual work
            # 1. Get all cart purchases using booking_id
            result = send_hotel_facilities(request.json.get('booking_id'), request.json.get('facilities_orders'))
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

def send_hotel_facilities(booking_id, facilities_orders):
    booking_result = invoke_http(booking_URL + "/" + booking_id)
    guest_details = {
        "email": booking_result['data']['email'],
        "guest_name": booking_result['data']['guest_name']
    }

    print('booking_result:', guest_details)

    code = booking_result["code"]
    if code not in range(200, 300):

        # if there are no bookings, return message
        return {
            "code": 404,
            "data": {"booking_result": booking_result}
        }

    for order in facilities_orders:
        f_order = {
            "item_id": order['item_id'],
            
            "price": order['item_price']
        }

    add_fb_result = invoke_http(cart_URL + "/add_fb/" + booking_id, method='POST', json=f_order)
    if add_fb_result['code'] not in range(200, 300):

            return {
                'code': 404,
                'status': 'failed to add facility booking'
            }

    return {
        "code": 201,
        "booking_result": {
            "email": booking_result['data']['email'],
            "guest_name": booking_result['data']['guest_name'],
            "status": "success"
        }
    }
# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for book facilities...")
    app.run(host="0.0.0.0", port=5300, debug=True)
