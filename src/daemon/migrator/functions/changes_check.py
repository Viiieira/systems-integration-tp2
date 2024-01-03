import sys
import time

from functions.execute_query import execute_query
from psycopg2 import OperationalError

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

def changes_check(connection):
    try:
        cursor = connection.cursor()

        # Execute a SELECT query to check for any changes on the table
        select_query = "SELECT id, file_name FROM imported_documents WHERE migrated = false"
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
