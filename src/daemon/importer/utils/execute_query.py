import psycopg2

def execute_query(query, params=None):
    connection = None
    cursor = None
    result = []

    try:
        connection = psycopg2.connect(user="is", password="is", host="db-xml", port="5432", database="is")
        cursor = connection.cursor()

        # In case the query has params, execute bind the values to the query
        cursor.execute(query, params) if params else cursor.execute(query)

        connection.commit()

        result = cursor.fetchall()

    except (Exception, psycopg2.Error) as error:
        print("Error executing the query:", error)
        result = f"Error: {error}"

    finally:
        if connection:
            cursor.close()
            connection.close()

    return result