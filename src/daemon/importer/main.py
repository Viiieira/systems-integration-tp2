import asyncio
import time
import uuid

from utils.execute_query import execute_query

import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

from utils.to_xml_converter import CSVtoXMLConverter

def get_csv_files_in_input_folder():
    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(CSV_INPUT_PATH) for f in filenames if
            os.path.splitext(f)[1] == '.csv']

def generate_unique_file_name(directory):
    return f"{directory}/{str(uuid.uuid4())}.xml"

def convert_csv_to_xml(in_path, out_path):
    converter = CSVtoXMLConverter(in_path)
    file = open(out_path, "w")
    file.write(converter.to_xml_str())

class CSVHandler(FileSystemEventHandler):
    def __init__(self, input_path, output_path):
        self._output_path = output_path
        self._input_path = input_path

        # Generate file creation events for existing files
        for file in [os.path.join(dp, f) for dp, dn, filenames in os.walk(input_path) for f in filenames]:
            event = FileCreatedEvent(os.path.join(CSV_INPUT_PATH, file))
            event.event_type = "created"
            self.dispatch(event)

    async def convert_csv(self, csv_path):
        # Check if the CSV file has already been converted
        converted_files = await self.get_converted_files()
        csv_filename = os.path.basename(csv_path)
        if csv_filename in converted_files:
            print(f"File '{csv_path}' has already been converted. Skipping.")
            return

        print(f"new file to convert: '{csv_path}'")


        # Generate a unique file name for the XML file
        xml_path = generate_unique_file_name(self._output_path)

        # Conversion from CSV to XML
        convert_csv_to_xml(csv_path, xml_path)
        print(f"new xml file generated: '{xml_path}'")

        # Update the converted_documents table
        query = "INSERT INTO converted_documents (src, file_size, dst) VALUES (%s, %s, %s)"
        params = (os.path.basename(csv_path), os.path.getsize(csv_path), os.path.basename(xml_path))
        execute_query(query, params)

        # Read the XML content from the generated file
        with open(xml_path, 'r') as xml_file:
            xml_content = xml_file.read()

        # Store the XML document into the imported_documents table
        query = "INSERT INTO imported_documents (file_name, xml) VALUES (%s, %s)"
        params = (os.path.basename(xml_path), xml_content)
        execute_query(query, params)

    async def get_converted_files(self):
        # Fetch the list of converted files from the database
        query = "SELECT src FROM converted_documents"
        result = execute_query(query)
        
        # Extract the 'src' values from the result
        converted_files = [row[0] for row in result]

        return converted_files

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".csv"):
            asyncio.run(self.convert_csv(event.src_path))


if __name__ == "__main__":

    CSV_INPUT_PATH = "/csv"
    XML_OUTPUT_PATH = "/xml"

    # create the file observer
    observer = Observer()
    observer.schedule(
        CSVHandler(CSV_INPUT_PATH, XML_OUTPUT_PATH),
        path=CSV_INPUT_PATH,
        recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
