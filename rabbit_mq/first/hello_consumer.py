#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'teng'
import pika
credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)

conn_broker = pika.BlockingConnection(conn_params)
channel = conn_broker.channel() # 获得信道
channel.exchange_declare(exchange="hello-exchange", # 声明交换器
                         exchange_type="direct",
                         passive=False,
                         durable=True,
                         auto_delete=False)
# 声明队列
channel.queue_declare(queue="hello-queue")
# 通过"hola"将队列和交换器绑定起来
channel.queue_bind(queue="hello-queue",
                   exchange="hello-exchange",
                   routing_key="hola")
# 用于处理传入的消息的函数
def msg_consumer(channel, method, header, body):
    channel.basic_ack(delivery_tag=method.delivery_tag)
    if body == "quit":
        # 退出消费
        channel.basic_cancel(consumer_tag="hello-consumer")
        channel.stop_consuming()
    else:
        print(body)
    return
# 订阅消费者
channel.basic_consume(msg_consumer,
                      queue="hello-queue",
                      consumer_tag="hello-consumer")
# 开始消费
channel.start_consuming()