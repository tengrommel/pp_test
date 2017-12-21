# coding:utf-8
import pika
credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)
conn_broker = pika.BlockingConnection(conn_params) # 建立到代理服务器的连接

channel=conn_broker.channel() # 获得信道
channel.exchange_declare(exchange="hello-exchange",  # 关联交换器
                         type="direct", 
                         passive=False,
                         durable=True,
                         auto_delete=False)
channel.queue_declare(queue='hello-queue') # 关联queue
channel.queue_bind(queue="hello-queue", # 绑定交换器和queue
                   exchange="hello-exchange",
                   routing_key="hola")

# 消费订阅 channel method header body
def msg_consumer(channel, method, header, body):
    channel.basic_ack(delivery_tag=method.delivery_tag)
    if body == "quit":
        channel.basic_cancel(consumer_tag="hello-consumer")
        channel.stop_consuming()
    else:
        print body
    return
channel.basic_consume(msg_consumer, queue="hello-queue", consumer_tag="hello-consumer")
channel.start_consuming()