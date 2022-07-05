from argparse import RawTextHelpFormatter
from time import sleep

import argparse
import logging
import pika
import sys


def on_message(channel, method_frame, header_frame, body):
    print(method_frame.delivery_tag)
    print(body)
    print(header_frame)
    LOG.info('Message has been received %s', body)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


if __name__ == '__main__':
    examples = sys.argv[0] + " -p 5672 -s rabbitmq "
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter,
                                     description='Run consumer.py',
                                     epilog=examples)
    parser.add_argument('-p', '--port', action='store', dest='port', help='The port to listen on.',default='5672')
    parser.add_argument('-s', '--server', action='store', dest='server', help='The RabbitMQ server.',default='rabbitmq')
    
    args = parser.parse_args()
    if args.port is None:
        print("Missing required argument: -p/--port")
        sys.exit(1)
    if args.server is None:
        print("Missing required argument: -s/--server")
        sys.exit(1)
    
    # sleep a few seconds to allow RabbitMQ server to come up
    sleep(5)
    logging.basicConfig(level=logging.INFO)
    LOG = logging.getLogger(__name__)
    credentials = pika.PlainCredentials('user', 'q0GVH1id3Ks9ukzc')
    parameters = pika.ConnectionParameters(args.server,
                                           int(args.port),
                                           '/',
                                           credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    
    channel.queue_declare('pc')
    channel.basic_consume(on_message, 'pc')
    
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()
