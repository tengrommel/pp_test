# -*- coding: utf-8 -*-
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='', #绑定到默认交换器
                      routing_key='task_queue', #路由键 'task_queue'
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode=2, # make message persistent
                      ))
print(" [x] Sent %r" % message)
connection.close()