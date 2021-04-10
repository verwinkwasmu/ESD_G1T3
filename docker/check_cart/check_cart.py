from flask import Flask, request, jsonify
from flask_cors import CORS

import os

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

cart_URL = os.environ.get("cart_URL") or "https://esdg1t3-cart.herokuapp.com/cart"
facility_URL = os.environ.get("facility_URL") or "https://esdg1t3-facility.herokuapp.com/facility"
room_service_URL = os.environ.get("room_service_URL") or "https://esdg1t3-roomservice.herokuapp.com/room_service"


@app.route("/check_cart", methods=['POST'])
def check_cart():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            booking_id = request.get_json()
            print("\nReceived a request to check cart in JSON:", booking_id)

            # do the actual work
            # 1. Get all cart purchases using booking_id
            result = processCheckCart(request.json.get('booking_id'))
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


def processCheckCart(booking_id):
    # 2. Send booking id to cart microservice to retrieve all cart items
    # Invoke cart microservice
    print('\n-----Invoking cart microservice-----')
    cart_result = invoke_http(cart_URL + "/booking/" + booking_id)
    print('cart_result:', cart_result)

    code = cart_result["code"]
    if code not in range(200, 300):

        # if there are no bookings, return message
        return {
            "code": 404,
            "data": {"cart_result": cart_result}
        }

    # 4. get all facilities & roomservices 
    all_facilities = invoke_http(facility_URL)
    all_room_services = invoke_http(room_service_URL)
    
    # 5. Put into dictionary for item_names
    facility_names = {}
    for facility in all_facilities['data']['facilities']:
        facility_names[facility['item_id']] = facility['item_name']

    room_service_names = {}
    for room_service in all_room_services['data']['room_services']:
        room_service_names[room_service['item_id']] = room_service['item_name']

    # 6. return all cart purchases with item_name
    for booking in cart_result['data']['bookings']:
        if 'rs' in booking['item_id']:
            booking['item_name'] = room_service_names[booking['item_id']]
        else:
            booking['item_name'] = facility_names[booking['item_id']]
    
    return {
        "code": 201,
        "all_bookings": cart_result['data']
    }


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for checking all items in cart...")
    port = int(os.environ.get('PORT', 5100)) or 5100
    app.run(host="0.0.0.0", port=port, debug=False)