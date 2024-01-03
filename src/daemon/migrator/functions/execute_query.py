import psycopg2

def execute_query(query, params=None, connection=None):
    cursor = None
    result = []

    try:
        if connection is None:
            raise ValueError("Connection parameter is required")

        cursor = connection.cursor()

        # In case the query has params, execute bind the values to the query
        cursor.execute(query, params) if params else cursor.execute(query)

        connection.commit()

        result = cursor.fetchall()

    except (Exception, psycopg2.Error) as error:
        print("Error executing the query:", error)
        result = f"Error: {error}"

    finally:
        if cursor:
            cursor.close()

    return result
