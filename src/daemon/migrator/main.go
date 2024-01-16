package main

import (
	"fmt"
	"log"

	"github.com/streadway/amqp"
)

const (
	RabbitMQURL = "amqp://is:is@rabbitMQ:5672/is"
	ImportQueue = "import_queue"
)

func checkError(err error) {
	if err != nil {
		log.Fatal(err)
	}
}

func main() {
	fmt.Println("Migrator: Listening for import tasks...")

	connection, err := amqp.Dial(RabbitMQURL)
	checkError(err)
	defer connection.Close()

	channel, err := connection.Channel()
	checkError(err)
	defer channel.Close()

	queue, err := channel.QueueDeclare(
		ImportQueue,
		false,
		false,
		false,
		false,
		nil,
	)
	checkError(err)

	messages, err := channel.Consume(
		queue.Name,
		"",
		true,
		false,
		false,
		false,
		nil,
	)
	checkError(err)

	for message := range messages {
		fmt.Printf("Received import task: %s\n", message.Body)

		fmt.Println("Import task processed.")
	}
}
