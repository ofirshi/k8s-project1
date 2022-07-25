from argparse import RawTextHelpFormatter
from time import sleep
import argparse
import logging
import pika
import sys


def main():
    try:
        examples = sys.argv[0] + " -p 5672 -s rabbitmq -m 'Hello' "
        parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter,
                                         description='Run producer.py',
                                         epilog=examples)
        parser.add_argument('-p', '--port', action='store', dest='port', help='The port to listen on.', default='5672')
        parser.add_argument('-s', '--server', action='store', dest='server', help='The RabbitMQ server.',
                            default='rabbitmq')
        parser.add_argument('-m', '--message', action='store', dest='message', help='The message to send',
                            required=False,
                            default='Hello')
        parser.add_argument('-r', '--repeat', action='store', dest='repeat',
                            help='Number of times to repeat the message',
                            required=False, default='30')
        
        args = parser.parse_args()
        if args.port is None:
            args.port='5672'
        if args.server is None:
            args.server='rabbitmq'
        # sleep a few seconds to allow RabbitMQ server to come up
        sleep(5)
        
        logging.basicConfig(level=logging.INFO)
        LOG = logging.getLogger(__name__)
        credentials = pika.PlainCredentials('guest', 'guest')
        parameters = pika.ConnectionParameters(args.server,
                                               int(args.port),
                                               '/',
                                               credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        q = channel.queue_declare('pc')
        q_name = q.method.queue
        
        # Turn on delivery confirmations
        channel.confirm_delivery()
        
        while True:  # Change the code of the producer to send infinite messages every 20 seconds
            for i in range(0, int(args.repeat)):
                if channel.basic_publish('', q_name, args.message):
                    LOG.info('Message has been delivered')
                else:
                    LOG.warning('Message NOT delivered')
                sleep(20)
        # connection.close()
    except Exception as e:
        print(e)
        exit(1)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
        exit(1)
