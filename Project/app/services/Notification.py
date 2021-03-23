import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# import email html file
with open('Email_content.html', 'r') as f:
    html_string = f.read()

# email address, subject and body
message = Mail(
    from_email='hotelenterprise@esd.sg',
    to_emails='weixiangtoh.2019@smu.edu.sg',
    subject='Testing sendgrid email services',
    html_content=html_string)

# sending email and printing status
try:
    print(os.environ.get('SENDGRID_API_KEY'))
    sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sendgrid_client.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)

except Exception as e:
    print(e)
