import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from flask import Flask, request
import json

# import email html file
# with open('Email_content.html', 'r') as f:
#     html_string = f.read()

app = Flask(__name__)


# email address, subject and body
# message = Mail(
#     from_email='hotelenterprise@esd.sg',
#     to_emails='jessie.ng.2019@smu.edu.sg',
#     subject='Testing sendgrid email services',
#     html_content=html_string)

# # sending email and printing status
# try:
#     print(os.environ.get('SENDGRID_API_KEY'))
#     sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
#     response = sendgrid_client.send(message)
#     print(response.status_code)
#     print(response.body)
#     print(response.headers)

# except Exception as e:
#     print(e)

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")

# sending email to to_email
# requires form to be filled up --> from_email, to_email, subject, html_content
@app.route("/notification", methods=['POST', 'GET'])
def mail():
    if request.method == "POST":
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        from_email = Email(request.form.get("from_email"))
        to_email = To(request.form.get("to_email"))
        subject = request.form.get("subject")
        content = Content("text/html", request.form.get("content"))

        message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=subject,
            html_content=content)
        
        response = sg.send(message)
        if response.status_code == 202:
            return message.get()
            # return "Email sent successfully!"
        else:
            return "Status Code: " + str(response.status_code)
    else:
        return """
        <html>
           <body>
              <form method = "POST">
                 <p>From: <input type = "text" name = "from_email" value="test@example.com" style="width: 500px;" /></p>
                 <p>To: <input type = "text" name = "to_email" value="jessie.ng.2019@smu.edu.sg" style="width: 500px;" /></p>
                 <p>Subject: <input type = "text" name = "subject" value="Sending with SendGrid is Fun" style="width: 500px;" /></p>
                 <p>Content: <input type ="text" name = "content" value="Hello! This is a ESD test :)" style="width: 500px;" /></p>
                 <p><input type = "submit" value = "send email" /></p>
              </form>
           </body>
        </html>
        """


if __name__ == "__main__":
    app.run(port=5004, debug=True)
