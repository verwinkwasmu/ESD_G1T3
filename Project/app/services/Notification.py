#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import amqp_setup
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from flask import Flask, request
import json

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
    mail()


# required signature for the callback; no return
def callback(channel, method, properties, body):
    print("\nReceived an error by " + __file__)
    processError(body)
    print()  # print a new line feed


def processError(errorMsg):
    print("Printing the error message:")
    try:
        error = json.loads(errorMsg)
        print("--JSON:", error)
    except Exception as e:
        print("--NOT JSON:", e)
        print("--DATA:", errorMsg)
    print()

# sending email to to_email
# requires form to be filled up --> from_email, to_email, subject, html_content
# @app.route("/notification", methods=['POST', 'GET'])

# import email html file
with open('Email_content.html', 'r') as f:
    html_string = f.read()

def mail():
    # email address, subject and body
    message = Mail(
        from_email='hotelenterprise@esd.sg',
        to_emails='jessie.ng.2019@smu.edu.sg',
        subject='Testing sendgrid email services',
        html_content=html_string)

    # sending email and printing status
    try:
        print(SENDGRID_API_KEY)
        sendgrid_client = SENDGRID_API_KEY
        response = sendgrid_client.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)

    except Exception as e:
        print(e)

    # if request.method == "POST":
    #     sg = SendGridAPIClient(SENDGRID_API_KEY)
    #     from_email = Email(request.form.get("from_email"))
    #     to_email = To(request.form.get("to_email"))
    #     subject = request.form.get("subject")
    #     content = Content("text/html", request.form.get("content"))

    #     message = Mail(
    #         from_email=from_email,
    #         to_emails=to_email,
    #         subject=subject,
    #         html_content=content)

    #     response = sg.send(message)
    #     if response.status_code == 202:
    #         return message.get()
    #         # return "Email sent successfully!"
    #     else:
    #         return "Status Code: " + str(response.status_code)
    # else:
    #     return """
    #     <html>
    #        <body>
    #           <form method = "POST">
    #              <p>From: <input type = "text" name = "from_email" value="test@example.com" style="width: 500px;" /></p>
    #              <p>To: <input type = "text" name = "to_email" value="jessie.ng.2019@smu.edu.sg" style="width: 500px;" /></p>
    #              <p>Subject: <input type = "text" name = "subject" value="Sending with SendGrid is Fun" style="width: 500px;" /></p>
    #              <p>Content: <input type ="text" name = "content" value="Hello! This is a ESD test :)" style="width: 500px;" /></p>
    #              <p><input type = "submit" value = "send email" /></p>
    #           </form>
    #        </body>
    #     </html>
    #     """


if __name__ == "__main__":
    # app.run(port=5004, debug=True)
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(
        monitorBindingKey, amqp_setup.exchangename))
    receiveNotification()
    mail()
