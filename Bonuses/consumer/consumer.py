import random
from argparse import RawTextHelpFormatter
from time import sleep

import argparse
import logging
import pika
import sys
import time
from prometheus_client import Counter, Summary, start_http_server

try:
    examples = sys.argv[0] + " -p 5672 -s rabbitmq "
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter,
                                     description='Run consumer.py',
                                     epilog=examples)
    parser.add_argument('-p', '--port', action='store', dest='port', help='The port to listen on.', default='5672')
    parser.add_argument('-s', '--server', action='store', dest='server', help='The RabbitMQ server.',
                        default='rabbitmq')
    
    args = parser.parse_args()
    if args.port == None:
        args.port = '5672'
        # print("Missing required argument: -p/--port")
        # sys.exit(1)
    if args.server == None:
        args.server = 'rabbitmq'
        # print("Missing required argument: -s/--server")
        # sys.exit(1)
except Exception as e:
    print(e)
    exit(1)

# sleep a few seconds to allow RabbitMQ server to come up
sleep(5)
logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


def on_message_received(ch, method, properties, body):
    processing_time = random.randint(1, 6)
    print(f'received: "{body}", will take {processing_time} to process')
    time.sleep(processing_time)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f'finished processing and acknowledged message')
    print("Massages left in the queue")
    print(f"properties {properties}")
    print(ch.queue_declare(queue='pc', exclusive=False, auto_delete=False).method.message_count)


def consumer(server, port):
    credentials = pika.PlainCredentials('guest', 'guest')
    connection_parameters = pika.ConnectionParameters(server,
                                                      port,
                                                      '/',
                                                      credentials)
    
    connection = pika.BlockingConnection(connection_parameters)
    
    channel = connection.channel()
    
    channel.queue_declare(queue='pc')
    
    channel.basic_qos(prefetch_count=1)
    
    channel.basic_consume(queue='pc', on_message_callback=on_message_received)
    print("Massages left in the queue")
    q = channel.queue_declare(queue='pc', exclusive=False, auto_delete=False).method.message_count
    print(q)
    
    print('Starting Consuming')
    channel.start_consuming()


REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

c = Counter('my_failures', 'Description of counter')
c.inc()  # Increment by 1
c.inc(1.6)  # Increment by given value


# Decorate function with metric.
@REQUEST_TIME.time()
def process_request(t, server, port):
    """A dummy function that takes some time."""
    time.sleep(t)
    consumer(server, port)


if __name__ == '__main__':
    try:
        # Start up the server to expose the metrics.
        start_http_server(9422)
        # Generate some requests.
        while True:
            process_request(random.random(), args.server, args.port)
    except Exception as e:
        print(e)
        exit(1)
