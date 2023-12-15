package main

import (
	"fmt"
	"io/ioutil"
	"strings"
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

func main() {
	fmt.Println("Hello, World!!")
	listXMLFiles()
}
