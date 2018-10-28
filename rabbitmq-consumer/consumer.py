import pika
import os
import time
import json


def pdf_process_function(msg):
    print("   processing...")
    print("   Received %r" % msg)

    d = msg.decode('ASCII')
    data = json.loads(d)
    print("data:", data)

    # print('Description: {}'.format(data['description']))

    print("command: {}".format(data['command']))
    print("vnf_pkg_path: {}".format(data['vnf_pkg_path']))
    print("vnf_pkg_filename: {}".format(data['vnf_pkg_filename']))

    #time.sleep(5) # delays for 5 seconds
    print("   processing finished")
    return


# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@172.20.0.2:5672/%2f')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='docker') # Declare a queue


# create a function which is called on incoming messages
def callback(ch, method, properties, body):
    pdf_process_function(body)


# set up subscription on the queue
channel.basic_consume(callback,
                      queue='docker',
                      no_ack=True)

# start consuming (blocks)
channel.start_consuming()
connection.close()