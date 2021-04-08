#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import amqp_setup
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from flask import Flask, request
import json

import threading
import time


app = Flask(__name__)


monitorBindingKey = '*.notification'
SENDGRID_API_KEY = os.environ.get(
    "SENDGRID_API_KEY") or "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"


def receiveNotification():
    amqp_setup.check_setup()

    queue_name = 'Notification'

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
        mail(json.loads(body))
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

def format_email(data):
    name = str(data["guest_name"])
    qty = str(data["quantity"])
    booking_type = str(data["type"])
    email_content = "<h4>Hello " + name + "!</h4>"

    if booking_type == "delay":
        body = "<p>We apologise for the delay regarding order:</p><p>Item Name: <strong>" + str(data["item_name"]) + "</strong></p><p>Quantity: <strong>" + qty + "</strong></p><p>Time ordered: " + str(data["date_time"]) + "</p><p>To make it up to you, here is a <strong>10%</strong> discount for your stay with us!</p>"

    elif booking_type == "facility":
        body = "<p>Here are your order details during your stay with us:</p><p>Item Name: <strong>" + str(data["item_name"]) + "</strong></p><p>Time ordered: " + str(data["date_time"]) + "</p>"

    else:
        body = "<p>Here are your order details during your stay with us:</p><p>Item Name: <strong>" + str(data["item_name"]) + "</strong></p><p>Quantity: <strong>" + qty + "</strong></p><p>Time ordered: " + str(data["date_time"]) + "</p>"


    end = "<p>For your reference, here is your order number <strong>#" + str(data["order_id"]) + "</strong> and your booking number <strong>#"+ str(data["booking_id"]) +"</p>"

    return email_content + body + end

def mail(json_msg):
    # email address, subject and body
    email_content = format_email(json_msg)
    booking_type = str(json_msg["type"])

    if booking_type == "facility":
        subject = "Facility Booking Confirmation [#" + str(json_msg["order_id"]) + "]"
    elif booking_type == "delay":
        subject = "Update on order/booking [#" + str(json_msg["order_id"]) + "]"
    else:
        subject = "Order Room Service Confirmation [#" + str(json_msg["order_id"]) + "]"

    message = Mail(
        from_email= From('dreamhotel@esd.sg', 'Dream Hotel'),
        to_emails= str(json_msg["email"]),
        subject= subject,
        html_content=email_content)

    # sending email and printing status
    try:
        print(SENDGRID_API_KEY)
        sendgrid_client = SendGridAPIClient(SENDGRID_API_KEY)
        response = sendgrid_client.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)

    except Exception as e:
        print(e)

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
    # port = int(os.environ.get('PORT', 5004))
    # app.run(host="0.0.0.0",port=port, debug=False)
