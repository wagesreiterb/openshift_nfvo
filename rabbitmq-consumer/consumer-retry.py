import pika
import json
import os
import time


RABBITMQ_SERVER = '172.20.0.2'  # hostname of rabbitmq-server


# create a function which is called on incoming messages
def callback(ch, method, properties, body):
    process_function(body)


def process_function(msg):
    print("   processing...")
    print("   Received %r" % msg)

    d = msg.decode('ASCII')
    data = json.loads(d)
    print("data:", data)

    # print('Description: {}'.format(data['description']))

    print("command: {}".format(data['command']))
    print("vnf_pkg_path: {}".format(data['vnf_pkg_path']))
    print("vnf_pkg_filename: {}".format(data['vnf_pkg_filename']))

    print("   processing finished")
    return


def on_message(channel, method_frame, header_frame, body):
    print(method_frame.delivery_tag)
    print(body)
    print()
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    return


## Assuming there are three hosts: host1, host2, and host3
#node1 = pika.URLParameters('amqp://' + RABBITMQ_SERVER)
#node2 = pika.URLParameters('amqp://' + RABBITMQ_SERVER)
#node3 = pika.URLParameters('amqp://' + RABBITMQ_SERVER)
#all_endpoints = [node1, node2, node3]
url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@' + RABBITMQ_SERVER + ':5672/%2f')
params = pika.URLParameters(url)


while True:
    try:
        print("Connecting...")
        ## Shuffle the hosts list before reconnecting.
        ## This can help balance connections.
        #random.shuffle(all_endpoints)
        # connection = pika.BlockingConnection(all_endpoints)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.basic_qos(prefetch_count=1)
        ## This queue is intentionally non-durable. See http://www.rabbitmq.com/ha.html#non-mirrored-queue-behavior-on-node-failure
        ## to learn more.
        # channel.queue_declare('docker', durable=False, auto_delete=True)
        channel.queue_declare(queue='docker')  # Declare a queue
        channel.basic_consume(callback,
                              queue='docker',
                              no_ack=True)
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
            connection.close()
            break
    #except pika.exceptions.ConnectionClosedByBroker:
        # Uncomment this to make the example not attempt recovery
        # from server-initiated connection closure, including
        # when the node is stopped cleanly
        #
        # break
    #    continue
    except pika.exceptions.ConnectionClosed:
        continue
    # Do not recover on channel errors
    except pika.exceptions.AMQPChannelError as err:
        print("Caught a channel error: {}, stopping...".format(err))
        break
    # Recover on all other connection errors
    except pika.exceptions.AMQPConnectionError:
        print("Connection was closed, retrying...")
        continue

    time.sleep(3)
