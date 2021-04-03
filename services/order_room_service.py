from flask import Flask, request, jsonify
from flask_cors import CORS

import os
import sys

import requests
from invokes import invoke_http

import amqp_setup
import pika
import json

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
            booking_details = request.get_json()
            print("\nReceived a request to order room service in JSON:",
                  booking_details)

            # do the actual work
            # 1. Get all cart purchases using booking_id
            result = processOrderRS(booking_details)
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


def processOrderRS(booking_details):
    print('\n-----Putting guest details-----')
    booking_id = booking_details['booking_id']
    email = booking_details['email']
    guest_name = booking_details['guest_name']

    room_service_orders = booking_details['room_service_orders']

    for order in room_service_orders:
        rs_order = {
            "item_id": order['item_id'],
            "rs_quantity": order['rs_quantity'],
            "price": order['item_price']
        }

        print('\n-----Invoking order microservice-----')
        add_rs_result = invoke_http(
            cart_URL + "/add_rs/" + booking_id, method='POST', json=rs_order)
        if add_rs_result['code'] not in range(200, 300):

            return {
                'code': 404,
                'status': 'failed to add room service'
            }

        # Invoke the order microservice
        print('add_rs_result:', add_rs_result)

        # Check the order result; if a failure, send it to the error microservice.
        code = add_rs_result["code"]
        email_details = {
            "email": email,
            "guest_name": guest_name,
            "quantity": order['rs_quantity'],
            "price": order['item_price'],
            "item_name" : order["item_name"],
            "date_time": add_rs_result["data"]["order_datetime"],
            "order_id": add_rs_result["data"]["order_id"],
            "booking_id": add_rs_result["data"]["booking_id"],
            "type": "room_service"
        }

        print('add_rs_result:', email_details)
        message = json.dumps(email_details)

        amqp_setup.check_setup()

        print('\n\n-----Publishing the (order notification) message with routing_key=order.notification-----')

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.notification",
                                         body=message, properties=pika.BasicProperties(delivery_mode=2))
        # make message persistent within the matching queues until it is received by some receiver
        # (the matching queues have to exist and be durable and bound to the exchange)

        # - reply from the invocation is not used;
        # continue even if this invocation fails
        print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(
            code), message)

        delay_content = {
            "order_id": add_rs_result["data"]["order_id"],
            "email": booking_result['data']['email'],
            "guest_name": booking_result['data']['guest_name'],
            "item_name" : order["item_name"],
        }
        delay_message = json.dumps(delay_content)

        waiting_time = order['waiting_time']

        if waiting_time == "30":
            print('\n\n-----Publishing the (short error service) message with routing_key=order.notification-----')

            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.short_error_service",
                                            body=delay_message, properties=pika.BasicProperties(delivery_mode=2))
            # make message persistent within the matching queues until it is received by some receiver
            # (the matching queues have to exist and be durable and bound to the exchange)

            # - reply from the invocation is not used;
            # continue even if this invocation fails
            print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(
                code), delay_message)
        else:
            print('\n\n-----Publishing the (long error service) message with routing_key=order.notification-----')

            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.long_error_service",
                                            body=delay_message, properties=pika.BasicProperties(delivery_mode=2))
            # make message persistent within the matching queues until it is received by some receiver
            # (the matching queues have to exist and be durable and bound to the exchange)

            # - reply from the invocation is not used;
            # continue even if this invocation fails
            print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(
                code), delay_message)


        


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
          " for ordering room service...")
    app.run(host="0.0.0.0", port=5200, debug=True)
