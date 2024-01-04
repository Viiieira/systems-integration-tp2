import sys
import time

import psycopg2
from psycopg2 import OperationalError

from functions.changes_check import changes_check
from functions.extract_countries import extract_countries
from functions.extract_provinces import extract_provinces

from functions.insert_countries import insert_countries
from functions.insert_provinces import insert_provinces

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
        # TODO: 1- Execute a SELECT query to check for any changes on the table
        try:
            changes_check(db_org)
        except Exception as e:
            print(f"An error occurred during TODO 1: {e}")


        # TODO: 2- Execute a SELECT queries with xpath to retrieve the data we want to store in the relational db
        country_data = extract_countries(db_org)
        province_data = extract_provinces(db_org)

        if country_data:
            for country in country_data:
                country = country.strip('{}').strip('"')
                print(f"> {country}")
        else:
            print("There are no countries")

        # Print province data
        if province_data:
            for province in province_data:
                print(f"> Province: {province['name']}, Country_ref: {province['country_ref']} , Latitude: {province['latitude']}, Longitude: {province['longitude']}")
        else:
            print("There are no provinces")

        # TODO: 3- Execute INSERT queries in the destination db
        try:
            # Using the function from the separate file to insert into the destination database
            insert_countries(db_dst, country_data)

            insert_provinces(db_dst, province_data)

        except Exception as e:
            print(f"Error executing INSERT queries: {e}")

        # !TODO: 4- Make sure we store somehow in the origin database that certain records were already migrated.
        #          Change the db structure if needed.

        db_org.close()
        db_dst.close()
        
        time.sleep(POLLING_FREQ)
