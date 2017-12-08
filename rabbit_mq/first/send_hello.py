#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'teng'

import pika, sys

credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)

conn_broker = pika.BlockingConnection(conn_params)
# 建立到服务器的连接
channel = conn_broker.channel()
# 创建信道
channel.exchange_declare(exchange="hello-exchange",
                         exchange_type="direct",
                         passive=False,
                         durable=True,
                         auto_delete=False)
# 声明交换机
msg = sys.argv[1]
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"
# 创建纯文本信息

channel.basic_publish(body=msg,
                      exchange="hello-exchange",
                      properties=msg_props,
                      routing_key="hola")
# 发布消息