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

type ProvinceData struct {
    Name    string `json:"name"`
	CountryName string `json:"country_name"`
}

type TasterData struct {
    Name    string `json:"name"`
	Twitter_handle    string `json:"twitter_handle"`
}

func checkError(err error) {
	if err != nil {
		log.Fatal(err)
	}
}

func callAPI(entityName string, message amqp.Delivery) error {
	client := resty.New()

	apiEndpoint := fmt.Sprintf("%s/%s", APIURL, entityName)

	switch entityName {
	case "Country":

		countryData := CountryData{Name: extractCountryName(message.Body)}
		resp, err := client.R().
			SetHeader("Content-Type", "application/json").
			SetBody(countryData).
			Post(apiEndpoint)

		if err != nil {
			return err
		}

		if resp.StatusCode() != 201 {
			return fmt.Errorf("API request failed with status code: %d", resp.StatusCode())
		}

	case "Province":

		provinceData, err := extractProvinceData(message.Body)

		resp, err := client.R().
			SetHeader("Content-Type", "application/json").
			SetBody(provinceData).
			Post(apiEndpoint)

		if err != nil {
			return err
		}

		if resp.StatusCode() != 201 {
			return fmt.Errorf("API request failed with status code: %d", resp.StatusCode())
		}
	case "Taster":

		tasterData, err := extractTasterData(message.Body)
		resp, err := client.R().
			SetHeader("Content-Type", "application/json").
			SetBody(tasterData).
			Post(apiEndpoint)

		if err != nil {
			return err
		}

		if resp.StatusCode() != 201 {
			return fmt.Errorf("API request failed with status code: %d", resp.StatusCode())
		}

	default:
		return fmt.Errorf("Unsupported entity: %s", entityName)
	}

	return nil
}

// Function to extract entity name from the message body
func extractEntityName(body []byte) string {
	// Convert the message body to a string
	messageStr := string(body)

	// Check if the message starts with "Import "
	if !strings.HasPrefix(messageStr, "Import ") {
		return ""
	}

	// Extract the entity name
	parts := strings.SplitN(messageStr, " ", 3)
	if len(parts) == 3 {
		entityName := strings.TrimSpace(parts[1]) // Trim spaces from the extracted entity name
		return strings.TrimSuffix(entityName, ":") // Trim the colon at the end
	}

	return ""
}

// Function to extract country name from the message body
func extractCountryName(body []byte) string {
	// Convert the message body to a string
	messageStr := string(body)

	// Check if the message starts with "Import country: "
	if !strings.HasPrefix(messageStr, "Import Country: ") {
		return ""
	}

	// Extract the country name
	countryName := strings.TrimPrefix(messageStr, "Import Country: ")

	return countryName
}

// Function to extract province data from the message body
func extractProvinceData(body []byte) (ProvinceData, error) {
	var provinceData ProvinceData

	// Convert the message body to a string
	messageStr := string(body)

	// Check if the message starts with "Import Province: "
	if !strings.HasPrefix(messageStr, "Import Province: ") {
		return provinceData, fmt.Errorf("Invalid Province message format")
	}

	// Extract the substring after "Import Province: "
	provinceInfo := strings.TrimPrefix(messageStr, "Import Province: ")

	// Split the provinceInfo into name and country name using ","
	parts := strings.SplitN(provinceInfo, ",", 2)
	if len(parts) != 2 {
		return provinceData, fmt.Errorf("Invalid Province message format")
	}

	// Extract the province name and country name
	provinceData.Name = strings.TrimSpace(parts[0])
	provinceData.CountryName = strings.TrimSpace(parts[1])

	return provinceData, nil
}


// Function to extract taster data from the message body
func extractTasterData(body []byte) (TasterData, error) {
	var tasterData TasterData

	// Convert the message body to a string
	messageStr := string(body)

	// Find the starting position of the name
	nameStart := strings.Index(messageStr, "Import Taster: ")
	if nameStart == -1 {
		return TasterData{}, fmt.Errorf("Invalid Taster message format")
	}

	// Extract the substring after "Import Taster: "
	nameAndHandle := strings.TrimSpace(messageStr[nameStart+15:])

	// Find the position of the comma (",") separating name and handle
	commaIndex := strings.Index(nameAndHandle, ",")
	if commaIndex == -1 {
		return TasterData{}, fmt.Errorf("Invalid Taster message format")
	}

	// Extract the name and Twitter handle
	tasterData.Name = strings.TrimSpace(nameAndHandle[:commaIndex])
	tasterData.Twitter_handle = strings.TrimSpace(nameAndHandle[commaIndex+1:])

	return tasterData, nil
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

		// Extract the entity name from the message body
		entityName := extractEntityName(message.Body)
		if entityName == "" {
			log.Printf("Invalid message format. Skipping.")
			continue
		}

		fmt.Printf("Extracted entity name: %s\n", entityName)
	
		// Call the API with the extracted entity name
		err := callAPI(entityName, message)
		if err != nil {
			log.Printf("Error calling API: %v", err)
			// Handle the error as needed
		}

		fmt.Println("Import task processed.")
	}
	
	
}
