#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script
from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http

import amqp_setup
import pika
import json

import threading
import time

app = Flask(__name__)
CORS(app)

monitorBindingKey = '*.error_service'
cart_URL = os.environ.get("cart_URL") or "https://esdg1t3-cart.herokuapp.com/cart"
booking_URL = environ.get('booking_URL') or "https://esdg1t3-booking.herokuapp.com/booking"

def receiveNotification():
    amqp_setup.check_setup()

    queue_name = 'Error_Service'
    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)
    # an implicit loop waiting to receive messages;
    amqp_setup.channel.start_consuming()
    # it doesn't exit by default. Use Ctrl+C in the command window to terminate it.


# required signature for the callback; no return
def callback(channel, method, properties, body):
    print("\nReceived an email request by " + __file__)
    try:
        print(body)
        checkTiming(json.loads(body))
    except:
        processError(body)


def processError(errorMsg):
    print("Printing the error message:")
    try:
        error = json.loads(errorMsg)
        print("--JSON:", error)
    except Exception as e:
        print("--NOT JSON:", e)
        print("--DATA:", errorMsg)
    print()


def checkTiming(data):
    order_id = str(data["order_id"])
    print('\n-----Invoking Cart microservice-----')
    order_result = invoke_http(
        cart_URL + "/order/" + order_id, method='GET')
    
    code = order_result['code']
    if order_result['code'] not in range(200, 300):

        return {
            'code': 404,
            'status': 'failed to get order'
        }
        
    delivered = order_result["data"]["rs_delivered_status"]

    if not delivered:
        email_details = {
            "email": data['email'],
            "guest_name": data['guest_name'],
            "quantity": order_result["data"]['rs_quantity'],
            "price": order_result["data"]['price'],
            "item_name" : data["item_name"],
            "date_time": order_result["data"]["order_datetime"],
            "order_id": order_result["data"]["order_id"],
            "booking_id": order_result["data"]["booking_id"],
            "type": "delay"
        }

        update_discount = invoke_http(booking_URL + "/" + str(order_result["data"]["booking_id"]), method='PUT')

        print('email_details:', email_details)
        message = json.dumps(email_details)

        amqp_setup.check_setup()

        print('\n\n-----Publishing the (delay notification) message with routing_key=delay.notification-----')

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="delay.notification",
                                         body=message, properties=pika.BasicProperties(delivery_mode=2))
        # make message persistent within the matching queues until it is received by some receiver
        # (the matching queues have to exist and be durable and bound to the exchange)

        # - reply from the invocation is not used;
        # continue even if this invocation fails
        print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(
            code), message)

# class ThreadingExample(object):
#     """ Threading example class
#     The run() method will be started and it will run in the background
#     until the application exits.
#     """

#     def __init__(self, interval=1):
#         """ Constructor
#         :type interval: int
#         :param interval: Check interval, in seconds
#         """
#         self.interval = interval

#         thread = threading.Thread(target=self.run, args=())
#         thread.daemon = True                            # Daemonize thread
#         thread.start()                                  # Start the execution

#     def run(self):
#         """ Method that runs forever """
#         while True:
#             # Do something
#             receiveNotification()

#             time.sleep(self.interval)

# example = ThreadingExample()
# time.sleep(3)
# print('Checkpoint')
# time.sleep(2)
# print('Bye')

if __name__ == "__main__":
    # app.run(port=5004,debug=True)
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(
        monitorBindingKey, amqp_setup.exchangename))
    receiveNotification()
    # port = int(os.environ.get('PORT', 5006))
    # app.run(host="0.0.0.0",port=port, debug=False)