package main

import (
	"database/sql"
	"encoding/xml"
	"fmt"
	"log"

	_ "github.com/lib/pq"
	"github.com/streadway/amqp"
)

type Wine struct {
	ID           int    `xml:"id,attr"`
	Name         string `xml:"name,attr"`
	Points       int    `xml:"points,attr"`
	Price        string `xml:"price,attr"`
	Variety      string `xml:"variety,attr"`
	ProvinceRef  int    `xml:"province_ref,attr"`
	TasterRef    int    `xml:"taster_ref,attr"`
	WineryRef    int    `xml:"winery_ref,attr"`
	Latitude     string `xml:"latitude,attr"`
	Longitude    string `xml:"longitude,attr"`
}

type Province struct {
	ID      int    `xml:"id,attr"`
	Name    string `xml:"name,attr"`
	CountryRef int `xml:"country_ref,attr"`
	Latitude  string `xml:"latitude,attr"`
	Longitude string `xml:"longitude,attr"`
	Wines    []Wine `xml:"Wines>Wine"`
}

type Country struct {
	ID       int       `xml:"id,attr"`
	Name     string    `xml:"name,attr"`
	Provinces []Province `xml:"Provinces>Province"`
}

type WineReviews struct {
	Countries []Country `xml:"Countries>Country"`
}

func sendMessageToBroker(countryName string) {
	rabbitMQUser := os.Getenv("RABBITMQ_DEFAULT_USER")
	rabbitMQPass := os.Getenv("RABBITMQ_DEFAULT_PASS")
	rabbitMQVHost := os.Getenv("RABBITMQ_DEFAULT_VHOST")
	rabbitMQHost := "localhost"
	rabbitMQPort := 5672

	// Create the connection string
	connectionString := fmt.Sprintf("amqp://%s:%s@%s:%d/%s", rabbitMQUser, rabbitMQPass, rabbitMQHost, rabbitMQPort, rabbitMQVHost)

	// Create a new AMQP connection
	conn, err := amqp.Dial(connectionString)
	CheckError(err)
	defer conn.Close()

	ch, err := conn.Channel()
	CheckError(err)
	defer ch.Close()

	q, err := ch.QueueDeclare(
		"import_queue", // Queue name
		false,          // Durable
		false,          // Delete when unused
		false,          // Exclusive
		false,          // No-wait
		nil,            // Arguments
	)
	CheckError(err)

	err = ch.Publish(
		"",           // Exchange
		q.Name,       // Routing key
		false,        // Mandatory
		false,        // Immediate
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        []byte(fmt.Sprintf("Import country: %s", countryName)),
		},
	)
	CheckError(err)
}

func checkUnmigratedFiles(db *sql.DB) {
	fmt.Println("Checking for unmigrated files...")
	rows, err := db.Query("SELECT file_name, xml FROM public.imported_documents WHERE migrated = FALSE AND deleted = FALSE")
	CheckError(err)
	defer rows.Close()

	fmt.Println("Unmigrated Files:")
	for rows.Next() {
		var fileName, xmlData string
		err := rows.Scan(&fileName, &xmlData)
		CheckError(err)

		fmt.Printf("\nFile Name: %s\n", fileName)

		// Parse the XML data
		var wineReviews WineReviews
		err = xml.Unmarshal([]byte(xmlData), &wineReviews)
		if err != nil {
			fmt.Printf("Error unmarshalling XML for file %s: %v\n", fileName, err)
			continue
		}

		// Process the parsed data
		processWineReviews(wineReviews)
	}
}

func processWineReviews(wineReviews WineReviews) {
	for _, country := range wineReviews.Countries {
		fmt.Printf("Country: %s\n", country.Name)
		sendMessageToBroker(country.Name) // Send message to the broker for each country

		for _, province := range country.Provinces {
			fmt.Printf("\tProvince: %s\n", province.Name)
			for _, wine := range province.Wines {
				fmt.Printf("\t\tWine: %s\n", wine.Name)
				// Add your logic here based on the wine entity
			}
		}
	}
}

func CheckError(err error) {
	if err != nil {
		log.Fatal(err)
	}
}

func main() {
	fmt.Println("Connecting to db.... ")
	connStr := "host=db-xml user=is password=is dbname=is sslmode=disable"
	db, err := sql.Open("postgres", connStr)
	CheckError(err)
	defer db.Close()

	if err := db.Ping(); err != nil {
		log.Fatal(err)
	}

	fmt.Println("\nSuccessfully connected to the database!")

	checkUnmigratedFiles(db)
}
