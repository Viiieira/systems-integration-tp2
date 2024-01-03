from functions.execute_query import execute_query

def extract_countries(connection):
    try:
        query = "SELECT xpath('/WineReviews/Countries/Country/@name', xml) AS country_name FROM public.imported_documents;"
        results = execute_query(query, connection=connection)

        if len(results) > 0:
            country_names_str = results[0][0]

            if country_names_str:
                return country_names_str.split(',')
            else:
                return []

        return []

    except Exception as e:
        print(f"Error extracting country names: {e}")
        return []
