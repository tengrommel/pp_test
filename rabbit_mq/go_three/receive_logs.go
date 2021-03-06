package main

import (
	"fmt"
	"log"
	"github.com/steadway/amqp"
)

func main()  {
	conn, err := amqp.Dial("amqp://guest:guest@localhost:5672/")
	failOnError(err, "Failed to connect to RabbitMQ")
	defer conn.Close()

	ch, err := conn.Channel()
	failOnError(err, "Failed to open a channel")
	defer conn.Close()

	err = ch.ExchangeDeclare(
		"logs",   // name
		"fanout", // type
		true,     // durable
		false,    // auto-deleted
		false,	  // internal
		false,    // no-wait
		nil,	  // argument
	)
	failOnError(err, "Failed to declare an exchange")

	q, err := ch.QueueDeclare(
		"", 	// name
		false,	// durable
		false,  // delete when usused
		true, 	// exclusive
		false,  // no-wait
		nil,    // argument
	)
	failOnError(err, "Failed to declare a queue")

	err = ch.QueueBind(
		q.Name, // queue name
		"",     // routing key
		"logs", // exchange
		false,
		nil)
	failOnError(err, "Failed to bind a queue")

	msgs, err := ch.Consume(
		q.Name, // queue
		"",     // consumer
		true,	// auto-ach
		false, 	// exclusive
		false,  // no-local
		false,  // no-wait
		nil,    // args
	)
	failOnError(err, "Failed to register a consumer")

	forever := make(chan bool)

	go func() {
		for d := range msgs{
			log.Printf(" [x] %s", d.Body)
		}
	}()
	
	log.Printf(" [*] Waiting for logs. To exit press CTRL+C")
	<-forever
}