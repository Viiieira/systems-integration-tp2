from functions.execute_query import execute_query

def insert_provinces(db_dst, province_data):
    try:
        # Handling the case when there are multiple country names
        if province_data:
            # Iterating over the list and inserting each country into the destination database
            for province, country_ref, latitude, longitude in province_data:
                # Removing curly braces if present
                province = province.strip('{}')

                # Check for None values and replace with appropriate values
                latitude = latitude if latitude is not None else 'NULL'
                longitude = longitude if longitude is not None else 'NULL'

                # Insert the province information into the destination database with point type for coordinates
                insert_query = f"INSERT INTO public.Province (name, id_country, coords) VALUES ('{province}', {country_ref}, ST_GeomFromText('POINT({latitude} {longitude})')) ON CONFLICT (name) DO NOTHING;"
                execute_query(insert_query, connection=db_dst)

            # Commit the transaction
            db_dst.commit()

    except Exception as e:
        print(f"Error executing INSERT queries: {e}")
