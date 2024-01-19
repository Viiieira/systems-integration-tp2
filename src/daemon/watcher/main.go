package main

import (
	"database/sql"
	"encoding/xml"
	"fmt"
	"log"

	_ "github.com/lib/pq"
	"github.com/streadway/amqp"
)

type Country struct {
	ID       int       `xml:"id,attr"`
	Name     string    `xml:"name,attr"`
	Provinces []Province `xml:"Provinces>Province"`
}

type Province struct {
	ID      int    `xml:"id,attr"`
	Name    string `xml:"name,attr"`
    CountryRef string `xml:"country_ref,attr"`
	Latitude  string `xml:"latitude,attr"`
	Longitude string `xml:"longitude,attr"`
	Wines    []Wine `xml:"Wines>Wine"`
}

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

type Taster struct {
    Name     string `xml:"name,attr"`
	Twitter_handle     string `xml:"twitter_handle,attr"`
}



type WineReviews struct {
	Countries []Country `xml:"Countries>Country"`
    Tasters   []Taster  `xml:"Tasters>Taster"`
}

func sendMessageToBroker(entityName string, message string, ch *amqp.Channel) bool { //message
    // Create the connection string
    connectionString := fmt.Sprintf("amqp://is:is@rabbitMQ:5672/is")

    // Create a new AMQP connection
    conn, err := amqp.Dial(connectionString)
    if err != nil {
        CheckError(err)
        return false
    }
    defer conn.Close()

    q, err := ch.QueueDeclare(
        "import_queue", // Queue name
        false,          // Durable
        false,          // Delete when unused
        false,          // Exclusive
        false,          // No-wait
        nil,            // Arguments
    )
    if err != nil {
        CheckError(err)
        return false
    }

    err = ch.Publish(
        "",           // Exchange
        q.Name,       // Routing key
        false,        // Mandatory
        false,        // Immediate
        amqp.Publishing{
            ContentType: "text/plain",
            Body:        []byte(fmt.Sprintf("Import %s: %s", entityName, message)),

        },
    )
    if err != nil {
        CheckError(err)
        return false
    }

    // Print success message
    fmt.Println("Successfully sent message to RabbitMQ")

    fmt.Printf("Import %s: %s\n", entityName, message)
    return true
}

func checkUnmigratedFiles(db *sql.DB, ch *amqp.Channel) {
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

		// Process the parsed data and send messages to the broker
		processWineReviews(wineReviews, ch)
	}
}

func processWineReviews(wineReviews WineReviews, ch *amqp.Channel) {
	for _, country := range wineReviews.Countries {
        countryMessage := fmt.Sprintf("%s", country.Name)

		// Send a message to the broker for each country
		if success := sendMessageToBroker("Country", countryMessage, ch); success {
			fmt.Printf("Successfully sent message for country: %s\n", country.Name)
               
		} else {
			fmt.Printf("Failed to send message for country: %s\n", country.Name)
		}

		for _, province := range country.Provinces {
            // Send a message to the broker for each province
			provinceMessage := fmt.Sprintf(" %s, %s, %s, %s, %s",
				province.Name, country.Name, province.CountryRef, province.Latitude, province.Longitude)

            // Send a message to the broker for each province
            if success := sendMessageToBroker("Province", provinceMessage, ch); success {
                fmt.Printf("Successfully sent message for province: %s\n", province.Name)
                
            } else {
                fmt.Printf("Failed to send message for province: %s\n", province.Name)
            }
        }
    }

    // Process Tasters
    for _, taster := range wineReviews.Tasters {
        tasterMessage := fmt.Sprintf("%s, %s",
            taster.Name, taster.Twitter_handle)

        // Send a message to the broker for each taster
        if success := sendMessageToBroker("Taster", tasterMessage, ch); success {
            fmt.Printf("Successfully sent message for taster: %s\n", taster.Name)
        } else {
            fmt.Printf("Failed to send message for taster: %s\n", taster.Name)
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

    // Create a new AMQP connection
    conn, err := amqp.Dial("amqp://is:is@rabbitMQ:5672/is")
    CheckError(err)
    defer conn.Close()

    ch, err := conn.Channel()
    CheckError(err)
    defer ch.Close()

    checkUnmigratedFiles(db, ch)
}
