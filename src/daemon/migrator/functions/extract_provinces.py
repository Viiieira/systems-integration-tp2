from functions.execute_query import execute_query

def extract_provinces(connection):
    try:
        query = (
            "SELECT "
            "xpath('/WineReviews/Countries/Country/Provinces/Province/@name', xml) AS province_name, "
            "xpath('/WineReviews/Countries/Country/Provinces/Province/@country_ref', xml) AS country_ref, "
            "xpath('/WineReviews/Countries/Country/Provinces/Province/@latitude', xml) AS latitude, "
            "xpath('/WineReviews/Countries/Country/Provinces/Province/@longitude', xml) AS longitude "
            "FROM public.imported_documents;"
        )

        results = execute_query(query, connection=connection)

        if len(results) > 0:
            province_data_list = []

            for row in results:
                province_name, country_ref, latitude, longitude = row
                province_data_list.append({
                    "name": province_name,
                    "country_ref": country_ref,
                    "latitude": latitude,
                    "longitude": longitude
                })

            return province_data_list
        else:
            return []

    except Exception as e:
        print(f"Error extracting province attributes: {e}")
        return []
