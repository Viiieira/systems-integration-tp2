import sys
import time

import psycopg2
from psycopg2 import OperationalError
from functions.execute_query import execute_query

POLLING_FREQ = int(sys.argv[1]) if len(sys.argv) >= 2 else 60

def print_psycopg2_exception(ex):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print("\npsycopg2 ERROR:", ex, "on line number:", line_num)
    print("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    print("\nextensions.Diagnostics:", ex.diag)

    # print the pgcode and pgerror exceptions
    print("pgerror:", ex.pgerror)
    print("pgcode:", ex.pgcode, "\n")

def check_for_changes_in_imported_documents(connection):
    try:
        cursor = connection.cursor()

        # TODO: Execute a SELECT query to check for any changes on the table
        select_query = "SELECT * FROM imported_documents WHERE migrated = false"
        cursor.execute(select_query)

        # Fetch the results
        results = cursor.fetchall()

        # Process the results (you may want to return or further process these results)
        for row in results:
            print(f"Found new document: {row}")

        # Commit the transaction
        connection.commit()

    except OperationalError as err:
        print_psycopg2_exception(err)
        connection.rollback()

    finally:
        if cursor:
            cursor.close()

if __name__ == "__main__":

    db_org = psycopg2.connect(host='db-xml', database='is', user='is', password='is')
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')

    while True:

        # Connect to both databases
        db_org = None
        db_dst = None

        try:
            db_org = psycopg2.connect(host='db-xml', database='is', user='is', password='is')
            db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
        except OperationalError as err:
            print_psycopg2_exception(err)

        if db_dst is None or db_org is None:
            continue

        print("Checking updates...")
        # !TODO: 1- Execute a SELECT query to check for any changes on the table
        try:
            query_todo1 = "SELECT id, file_name FROM imported_documents WHERE migrated = false"
            results_todo1 = execute_query(query_todo1, connection=db_org)
            print("Query Results for TODO 1:")
            for row in results_todo1:
                document_id, file_name = row
                print(f"Found new document (ID: {document_id}) with file name: {file_name}")

        except Exception as e:
            print(f"An error occurred during TODO 1: {e}")


        # !TODO: 2- Execute a SELECT queries with xpath to retrieve the data we want to store in the relational db
        try:
            query = "SELECT xpath('/WineReviews/Countries/Country/@*', xml) AS country_info FROM public.imported_documents;"

            results = execute_query(query, connection=db_org)

            if len(results) > 0:
                # Extracting the country information from the result
                country_info_str = results[0][0]

                # Handling the case when there are multiple country information
                if country_info_str:
                    country_info_list = country_info_str.split(',')

                    # Iterating over the list and printing each country information without curly braces
                    for country_info in country_info_list:
                        # Removing curly braces if present
                        country_info = country_info.strip('{}')

                        print(f"> {country_info.strip()}")
                else:
                    print("There are no countries")
            else:
                print("There are no countries in the result")

        except Exception as e:
            print(f"Error executing query: {e}")


        # !TODO: 3- Execute INSERT queries in the destination db
    

        # !TODO: 4- Make sure we store somehow in the origin database that certain records were already migrated.
        #          Change the db structure if needed.

        db_org.close()
        db_dst.close()
        
        time.sleep(POLLING_FREQ)
