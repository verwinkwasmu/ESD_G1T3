from flask import Flask, request, jsonify
from flask_cors import CORS

import os

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

booking_URL = "http://localhost:5000/booking"
cart_URL = "http://localhost:5001/cart"
room_service_URL = "http://localhost:5003/room_service"


@app.route("/order_room_service", methods=['POST'])
def order_room_service():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            booking_id = request.get_json()
            print("\nReceived a request to order room service in JSON:", booking_id)

            # do the actual work
            # 1. Get all cart purchases using booking_id
            result = processOrderRS(request.json.get('booking_id'))
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


def processOrderRS(booking_id):
    # 2. Send booking id to booking microservice to booking info (guest_name and email)
    # Invoke booking microservice
    print('\n-----Invoking booking microservice-----')
    booking_result = invoke_http(booking_URL + "/" + booking_id)
    print('booking_result:', booking_result)
    print("hello!!!")

    code = booking_result["code"]
    if code not in range(200, 300):

        # if there are no bookings, return message
        return {
            "code": 404,
            "data": {"booking_result": booking_result}
        }

    # # 4. get all facilities & roomservices 
    # all_facilities = invoke_http(facility_URL)
    # all_room_services = invoke_http(room_service_URL)
    
    # # 5. Put into dictionary for item_names
    # facility_names = {}
    # for facility in all_facilities['data']['facilities']:
    #     facility_names[facility['item_id']] = facility['item_name']

    # room_service_names = {}
    # for room_service in all_room_services['data']['room_services']:
    #     room_service_names[room_service['item_id']] = room_service['item_name']

    # # 6. return all cart purchases with item_name
    # for booking in cart_result['data']['bookings']:
    #     if 'rs' in booking['item_id']:
    #         booking['item_name'] = room_service_names[booking['item_id']]
    #     else:
    #         booking['item_name'] = facility_names[booking['item_id']]
    
    return {
        "code": 201,
        "booking_result": booking_result['data']
    }


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for ordering room service...")
    app.run(host="0.0.0.0", port=5200, debug=True)