package main

import (
	"fmt"
	"log"
	"strings"
	"gopkg.in/resty.v1"

	"github.com/streadway/amqp"
)

const (
	RabbitMQURL = "amqp://is:is@rabbitMQ:5672/is"
	ImportQueue = "import_queue"
	APIURL = "http://api-entities:8080"
)

type CountryData struct {
    Name    string `json:"name"`
}


func checkError(err error) {
	if err != nil {
		log.Fatal(err)
	}
}

func callAPI(countryData CountryData) error {
    client := resty.New()

    resp, err := client.R().
        SetHeader("Content-Type", "application/json").
        SetBody(countryData).
        Post(APIURL + "/Country")

    if err != nil {
        return err
    }

    if resp.StatusCode() != 200 {
        return fmt.Errorf("API request failed with status code: %d", resp.StatusCode())
    }

    return nil
}

// Function to extract country name from the message body
func extractCountryName(body []byte) string {
	// Convert the message body to a string
	messageStr := string(body)

	// Check if the message starts with "Import country: "
	if !strings.HasPrefix(messageStr, "Import country: ") {
		return ""
	}

	// Extract the country name
	countryName := strings.TrimPrefix(messageStr, "Import country: ")

	return countryName
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
	
		// Extract the country name from the message body
		countryName := extractCountryName(message.Body)
		if countryName == "" {
			log.Printf("Invalid message format. Skipping.")
			continue
		}
	
		fmt.Printf("Extracted country name: %s\n", countryName)
	
		// Call the API with the extracted country name
		err := callAPI(CountryData{Name: countryName})
		if err != nil {
			log.Printf("Error calling API: %v", err)
			// Handle the error as needed
		}
	
		fmt.Println("Import task processed.")
	}
	
	
}
