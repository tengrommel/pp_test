# -*- coding:utf-8 -*-
import pika, sys
from pika import spec
credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("localhost",
                                        credentials=credentials)

conn_broker = pika.BlockingConnection(conn_params)
channel = conn_broker.channel()
def confirm_handler(frame): #发送方确认模式处理器
    # spec检查selectOk
    if type(frame.method) == spec.Confirm.SelectOk:
        print "Channel in 'confirm' mode."
    # 消息丢失
    elif type(frame.method) == spec.Basic.Nack:
        if frame.method.delivery_tag in msg_ids:
            print "Message lost!"
    # 消息确认成功
    elif type(frame.method) == spec.Basic.Ack:
        if frame.method.delivery_tag in msg_ids:
            print "Confirm received!"
            msg_ids.remove(frame.method.delivery_tag)

# 创建时创建回调函数
channel.confirm_delivery(callback=confirm_handler)
# 将信道设置为confirm模式
msg = sys.argv[1]
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"

msg_ids = [] # 设置消息ID追踪器
channel.basic_publish(body=msg,
                      exchange="hello-exchange", #绑定到交换器
                      properties=msg_props,
                      routing_key="hola") # 发布消息
msg_ids.append(len(msg_ids) + 1) # 将消息ID添加到追踪列表
channel.close()