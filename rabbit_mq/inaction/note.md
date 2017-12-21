# rabbitmq

## 理解消息通信

### 从底部开始构造：队列

#### RabbitMQ进行交流。服务必须要完成两个任务：

    - (1)存储代客票ID以及对应的车辆停放泊车位
        > 你所提供的服务将扮演消费者的角色。
        它订阅Rabbit队列，等待“存放票”消息。该消息包含票ID和泊车位号码。
    - (2)返回指定代客票ID对应的泊车位。
        > 你所提供的服务即是消费者也是生产者的角色。
        它需要接收消息来获取特定代客票ID，然后它需要发布一个包含对应泊车位号码的应答消息。

#### 从底部开始构造：队列

>AMQP消息路由必须有三部分：交换器、队列和绑定。生产者把消息发布到交换器上；消息最终到达队列，并被消费者接收；<br>
绑定决定了消息如何从路由器路由到特定的队列。

##### 消费者通过下面两种方式从特定的队列中接收消息

- （1）通过AMQP的basic.consume命令订阅。这样做会将信道置为接收模式，直到取消对队列的订阅为止。

     *订阅了消息后，消费者在消费（或者拒绝）最近接收的那条消息后，就能从队列中（可用的）自动接收吓一条消息。*<br>
     *如果消费者处理队列消息，并且/或者需要在消息一到达队列时就自动接收的话，你应该使用basic.consume。*

- （2）某些时候，你只想从队列获得单条消息而不是持续订阅。
    *向队列请求单条消息是通过AMQP的basic.get命令实现的。这样做可以让消费者接收队列中的下一条消息。*

- 当rabbit队列拥有多个消费者时，队列收到的消息将以循环(round-robin)的方式发送给消费者。
    *basic.ack*

#### 联合起来：交换器和绑定
RabbitMQ将会决定消息该投递到哪个队列，这些规则被称作路由键(routing key)。<br>
队列通过路由键绑定到交换器。<br>

#### 交换机的四种类型

- direct
  *如果路由匹配的话，消息就被投递到对应的队列。*
  > channel->basic_publish($msg, '', 'queue-name');<br>
  第一个参数是你想要发送的消息内容；<br>
  第二个参数是一个空的字符串，指定了默认交换器；<br>
  而第三个就是路由键了。
- fanout
  *当你发送一条消息到fanout交换器时，它会把消息投递给所有附加在此的交换器上的队列。*
- topic
  *它使得来自不同源头的消息能够到达同一个队列。*
  >channel->basic_publish($msg, 'logs-exchange', 'error.msg-inbox');<br>
  channel->queue_bind('msg-inbox-errors', 'logs-exchange', 'error.msg-index');<br>
  channel->queue_bind('all-logs', 'logs-exchange', '#');<br>
- header

#### 多租户模式：虚拟机和隔离

- vhost
>每一个RabbitMQ服务器都能创建虚拟消息服务器，我们称之为虚拟主机(vhost)。
*作用：通过在各个实例间提供逻辑上分离，允许你为不同应用程序安全保密地运行数据。*
*vhost是唯一无法通过AMQP协议创建的基元*
>sudo rabbitmqctl set_user_tags guest  administrator management<br>
sudo rabbitmqctl set_permissions -p vhost_teng guest '.*' '.*' '.*'

#### 持久化

- 每个队列和交换机的durable属性(false)
- 避免消息从rabbit崩溃中丢失
    -把它的投递模式选项设置为2
    -发送到持久化的交换器
    -到达持久化的队列

## rabbitmq 管理

>Erlang天生就能让应用程序无须知道对方是否在同一台机器上即可相互通信。<br>
对RabbitMQ来说，这让集群和可靠的消息路由变得简单。

### 启动节点

>与jvm相似，Erlang也有虚拟机，而虚拟机的每个实例我们称之为节点(node)。<br>
不同于JVM，多个erlang应用程序可以运行在同一个节点之上。<br>
更重要的是，节点之间可以进行本地通信（不管它们是否真的在同一台服务器上）。<br>
比如说一个运行在asparagus节点上的应用程序可以调用artichoke节点上的应用程序方法，就是像调用本地函数一样。<br>
同时，如果应用程序由于某些原因崩溃了，Erlang节点会自动尝试重启应用程序（前提是erlang没有崩溃）。<br>

### 停止节点

rabbitmqctl stop 
>rabbitmqctl会和本地节点通信并指示其干净地关闭。同时关闭rabbit、mnesia和os_mon。

- 关闭和重启应用程序：有何差别:
>rabbitmqctl stop_app 只关闭rabbit应用程序

- Rabbit配置文件
>/etc/rabbitmq/rabbitmq.config

### 修复Rabbit： 疑难解答