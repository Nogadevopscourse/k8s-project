from argparse import RawTextHelpFormatter
from time import sleep

import argparse
import logging
import pika
import sys


def on_message(channel, method_frame, header_frame, body):
    print (method_frame.delivery_tag)
    print (body)
    print
    LOG.info('Message has been received %s', body)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


if __name__ == '__main__':
    examples = sys.argv[0] + " -p 5672 -s rabbitmq "
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter,
                                 description='Run consumer.py',
                                 epilog=examples)
    parser.add_argument('-p', '--port', action='store', dest='port', help='The port to listen on.')
    parser.add_argument('-s', '--server', action='store', dest='server', help='The RabbitMQ server.')
    parser.add_argument('-u', '--user', action='store', dest='user', help='The RabbitMQ user.')
    parser.add_argument('-ps', '--password', action='store', dest='password', help='The RabbitMQ password.')


    args = parser.parse_args()
    if args.port == None:
        print ("Missing required argument: -p/--port")
        sys.exit(1)
    if args.server == None:
        print ("Missing required argument: -s/--server")
        sys.exit(1)
    if args.user == None:
        print ("Missing required argument: -u/--user")
        sys.exit(1)
    if args.password == None:
        print ("Missing required argument: -ps/--password")
        sys.exit(1)

    # sleep a few seconds to allow RabbitMQ server to come up
    sleep(5)
    logging.basicConfig(level=logging.INFO)
    LOG = logging.getLogger(__name__)
    credentials = pika.PlainCredentials(args.user, args.password)
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
