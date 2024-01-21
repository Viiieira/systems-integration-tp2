package main

import (
	"database/sql"
	"encoding/xml"
	"fmt"
	"log"
    "time" 

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
	Wines    []Wine `xml:"Wines>Wine"`
}

type Wine struct {
	ID           int    `xml:"id,attr"`
	Name         string `xml:"name,attr"`
	Points       int    `xml:"points,attr"`
	Price        string `xml:"price,attr"`
	Variety      string `xml:"variety,attr"`
    TasterRef    int    `xml:"taster_ref,attr"`
	WineryRef    int    `xml:"winery_ref,attr"`
}

type Winery struct {
	ID   int    `xml:"id,attr"`
	Name string `xml:"name,attr"`
}

type Taster struct {
    ID              int    `xml:"id,attr"`
    Name     string `xml:"name,attr"`
	Twitter_handle     string `xml:"twitter_handle,attr"`
}

type WineReviews struct {
	Countries []Country `xml:"Countries>Country"`
    Tasters   []Taster  `xml:"Tasters>Taster"`
    Wineries  []Winery  `xml:"Wineries>Winery"`
}

func sendProvinceUpdateMessageToBroker(provinceName string, ch *amqp.Channel) bool {
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
        "coords_queue",          
        false,                   // Durable
        false,                   // Delete when unused
        false,                   // Exclusive
        false,                   // No-wait
        nil,                     // Arguments
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
            Body:        []byte(fmt.Sprintf("Get coordinates for Province: %s", provinceName)),
        },
    )
    if err != nil {
        CheckError(err)
        return false
    }

    // Print success message
    fmt.Println("Successfully sent province update message to RabbitMQ")

    fmt.Printf("Get coordinates for Province: %s\n", provinceName)
    return true
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

        // Mark the file as migrated
		markFileAsMigrated(db, fileName)
	}
}

// Function to mark a file as migrated
func markFileAsMigrated(db *sql.DB, fileName string) {
	_, err := db.Exec("UPDATE public.imported_documents SET migrated = TRUE WHERE file_name = $1", fileName)
	if err != nil {
		fmt.Printf("Error updating migration status for file %s: %v\n", fileName, err)
	} else {
		fmt.Printf("File %s marked as migrated.\n", fileName)
	}
}

func processWineReviews(wineReviews WineReviews, ch *amqp.Channel) {

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

    for _, winery := range wineReviews.Wineries {
        // Send a message to the broker for each winery
        wineryMessage := fmt.Sprintf("%s",
            winery.Name)

        if success := sendMessageToBroker("Winery", wineryMessage, ch); success {
            fmt.Printf("Successfully sent message for winery: %s\n", winery.Name)
        } else {
            fmt.Printf("Failed to send message for winery: %s\n", winery.Name)
        }
    }

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
			provinceMessage := fmt.Sprintf("%s, %s ",
				province.Name, country.Name)

            // Send a message to the broker for each province
            if success := sendMessageToBroker("Province", provinceMessage, ch); success {
                fmt.Printf("Successfully sent message for province: %s\n", province.Name)
                
            } else {
                fmt.Printf("Failed to send message for province: %s\n", province.Name)
            }

            // Send a message to the new queue for each province
            if success := sendProvinceUpdateMessageToBroker(province.Name, ch); success {
                fmt.Printf("Successfully sent province update message for province: %s\n", province.Name)
            } else {
                fmt.Printf("Failed to send province update message for province: %s\n", province.Name)
            }

            for _, wine := range province.Wines {
                // Send a message to the broker for each province
                wineMessage := fmt.Sprintf("%s, %d, %s, %s, %s, %s, %s",
                    wine.Name, wine.Points, wine.Price, wine.Variety, province.Name, getTasterName(wine.TasterRef, wineReviews), getWineryName(wine.WineryRef, wineReviews))

                // Send a message to the broker for each province
                if success := sendMessageToBroker("Wine", wineMessage, ch); success {
                    fmt.Printf("Successfully sent message for wine: %s\n", wine.Name)
                    
                } else {
                    fmt.Printf("Failed to send message for wine: %s\n", wine.Name)
                }
            }
        }
    }
    
}

// Function to get winery name based on winery reference
func getWineryName(wineryRef int, wineReviews WineReviews) string {
    for _, winery := range wineReviews.Wineries {
        if winery.ID == wineryRef {
            return winery.Name
        }
    }
    return "Unknown Winery"
}

// Function to get taster name based on taster reference
func getTasterName(tasterRef int, wineReviews WineReviews) string {
    for _, taster := range wineReviews.Tasters {
        if taster.ID == tasterRef {
            return taster.Name
        }
    }
    return "Unknown Taster"
}

func CheckError(err error) {
	if err != nil {
		log.Fatal(err)
	}
}

func main() {
    var isMigrating bool

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

    for {
        // Check if a file is currently being migrated
        if isMigrating {
            fmt.Println("Waiting for the current file processing to complete...")
            time.Sleep(5 * time.Second)
            continue
        }

        // Print a message indicating that the program is actively listening
        fmt.Println("Listening for new files to migrate...")

        // Set the migrating flag to true
        isMigrating = true

        // Check for new unmigrated files
        checkUnmigratedFiles(db, ch)

        // Set the migrating flag to false
        isMigrating = false

        // Sleep for some time before checking again
        time.Sleep(30 * time.Second)
    }
}
