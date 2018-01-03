package main

import (
	"log"
	"github.com/streadway/amqp"
)

func failOnError(err error, msg string)  {
	if err != nil{
		log.Fatalf("%s: %s", msg, err)
	}
}

func main()  {
	conn, err := amqp.Dial("amqp://guest:guest@localhost:5672/")
	failOnError(err, "Failed to connect to RabbitMQ")
	defer conn.Close()

	ch, err := conn.Channel()
	failOnError(err, "Failed to open a channel")
	defer ch.Close()

	q, err := ch.QueueDeclare(
		"hello",// name
		false, // durable
		false, // delete when unused
		false, // exclusive
		false, // no-wait
		nil,   // arguments
	)
	failOnError(err, "Failed to declare a queue")

	msgs, err := ch.Consume(
		q.Name, // queue
		"",		// exchange
		true,	// auto-ack
		false,	// exclusive
		false,	// no-local
		false,	// no-wait
		nil,	// args
	)
	failOnError(err, "Failed to register a consumer")

}