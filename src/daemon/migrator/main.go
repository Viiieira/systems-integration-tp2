package main

import (
	"fmt"
	"io/ioutil"
	"strings"
	"database/sql"

	_ "github.com/lib/pq"
)

func listXMLFiles() {
	files, err := ioutil.ReadDir("/xml")
	if err != nil {
		fmt.Printf("Error accessing /xml: %s\n", err)
		return
	}
	
	for _, f := range files {
		if strings.HasSuffix(f.Name(), ".xml") {
			fmt.Printf("\t> %s\n", f.Name())
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
	connStr := "host=localhost port=10001 user=is dbname=is password='is' sslmode=disable"
	db, err := sql.Open("postgres", connStr)
	CheckError(err)
	defer db.Close()

	if err := db.Ping(); err != nil {
		log.Fatal(err)
	}

	fmt.Println("\nSuccessfully connected to the database!")

	fmt.Println("Hello, World!!")
	listXMLFiles()
}
