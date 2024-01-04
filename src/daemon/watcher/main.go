package main

import (
	"fmt"
	"database/sql"
	_ "github.com/lib/pq"
	"log"
)


func checkUnmigratedFiles(db *sql.DB) {
	fmt.Println("Checking for unmigrated files...")
	rows, err := db.Query("SELECT file_name FROM public.imported_documents WHERE migrated = FALSE AND deleted = FALSE")
	CheckError(err)
	defer rows.Close()

	fmt.Println("Unmigrated Files:")
	for rows.Next() {
		var fileName string
		err := rows.Scan(&fileName)
		CheckError(err)
		fmt.Printf("\t> %s\n", fileName)
	}

	err = rows.Err()
	CheckError(err)
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
