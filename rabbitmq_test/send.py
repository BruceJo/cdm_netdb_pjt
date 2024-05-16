#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello1')

channel.basic_publish(exchange='', routing_key='hello1', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()
