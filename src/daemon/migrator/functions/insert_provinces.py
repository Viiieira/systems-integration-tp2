from functions.execute_query import execute_query

def insert_provinces(db_dst, province_data):
    try:
        # Handling the case when there are multiple provinces
        if province_data:
            # Iterating over the list and inserting each province into the destination database
            for province in province_data:
                # Extracting relevant information from the province data
                name = province.get('name', '')
                latitude = province.get('latitude', '')
                longitude = province.get('longitude', '')
                country_id = province.get('country_id', '')

                if not name or not latitude or not longitude or not country_id:
                    print(f"Skipping insertion for province. Missing required information.")
                    continue

                # Insert the province information into the destination database
                insert_query = f"INSERT INTO public.Province (name, coords, id_country) VALUES " \
                               f"('{name}', point({longitude}, {latitude}), '{country_id}') ON CONFLICT (name) DO NOTHING;"
                execute_query(insert_query, connection=db_dst)

            # Commit the transaction
            db_dst.commit()

    except Exception as e:
        print(f"Error executing INSERT queries for provinces: {e}")
