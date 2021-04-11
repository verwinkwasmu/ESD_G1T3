import pika
from os import environ

hostname = environ.get('rabbit_host') or '0.0.0.0'
port = environ.get('rabbit_port') or 5672

# url = "http://54.169.201.130:5672"
# params = pika.URLParameters(url)
# connection = pika.BlockingConnection(params)

# connect to the broker and set up a communication channel in the connection
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=hostname, port=port,
        heartbeat=3600, blocked_connection_timeout=3600, # these parameters to prolong the expiration time (in seconds) of the connection
))

############   Main Channel and Exchange   #############
channel = connection.channel()
# Set up the exchange if the exchange doesn't exist
# - use a 'topic' exchange to enable interaction
exchangename="order_topic"
exchangetype="topic"
channel.exchange_declare(exchange=exchangename, exchange_type=exchangetype, durable=True)
    # 'durable' makes the exchange survive broker restarts

############   Notification queue   #############
#delcare Notification queue
queue_name = 'Notification'
channel.queue_declare(queue=queue_name, durable=True) 
    # 'durable' makes the queue survive broker restarts

#bind Notification queue
channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='*.notification')
    # bind the queue to the exchange via the key
    # any routing_key with two words and ending with '.notification' will be matched

############   Delay Exchange   #############
# Create our delay channel.
delay_exchangename="delay"
delay_exchangetype="x-delayed-message"
channel.exchange_declare(exchange=delay_exchangename, exchange_type=delay_exchangetype, durable=True, arguments={
  'x-delayed-type': "topic" 
})
############   Error_Service queue   #############
#delcare Error_Service queue
queue_name = 'Error_Service'
channel.queue_declare(queue=queue_name, durable=True) 
    # 'durable' makes the queue survive broker restarts

#bind Error_Service queue
channel.queue_bind(exchange=delay_exchangename, queue=queue_name, routing_key='*.error_service')
    # bind the queue to the exchange via the key
    # any routing_key with two words and ending with '.error_service' will be matched

"""
This function in this module sets up a connection and a channel to a local AMQP broker,
and declares a 'topic' exchange to be used by the microservices in the solution.
"""
def check_setup():
    global connection, channel, hostname, port, exchangename, exchangetype
    # global connection, channel, url, params, exchangename, exchangetype

    if not is_connection_open(connection):
        # connection = pika.BlockingConnection(params)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
    if channel.is_closed:
        channel = connection.channel()
        channel.exchange_declare(exchange=exchangename, exchange_type=exchangetype, durable=True)


def is_connection_open(connection):
    try:
        connection.process_data_events()
        return True
    except pika.exceptions.AMQPError as e:
        print("AMQP Error:", e)
        print("...creating a new connection.")
        return False
