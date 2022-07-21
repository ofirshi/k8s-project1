import random
import time
import pika
from prometheus_client import Counter, Summary, start_http_server

def on_message_received(ch, method, properties, body):
    processing_time = random.randint(1, 6)
    print(f'received: "{body}", will take {processing_time} to process')
    time.sleep(processing_time)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f'finished processing and acknowledged message')
    print("Massages left in the queue")
    print(ch.queue_declare(queue='pc', exclusive=False, auto_delete=False).method.message_count)


def consumer():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection_parameters = pika.ConnectionParameters('rabbitmq',
                                                      5672,
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
def process_request(t):
    """A dummy function that takes some time."""
    #    time.sleep(t)
    consumer()


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(9422)
    # Generate some requests.
    while True:
        process_request(random.random())
