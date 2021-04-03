#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script
from flask import Flask, request, jsonify
from flask_cors import CORS

import os
import sys

import requests
from invokes import invoke_http

import amqp_setup
import pika
import json
from error_service import *


app = Flask(__name__)
CORS(app)


monitorBindingKey = '*.long_error_service'
queue_name = 'Long_Error_Service'


if __name__ == "__main__":
    # app.run(port=5004,debug=True)
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(
        monitorBindingKey, amqp_setup.exchangename))
    receiveNotification(queue_name)