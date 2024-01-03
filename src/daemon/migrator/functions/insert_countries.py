from functions.execute_query import execute_query

def insert_countries(db_dst, country_data):
    try:
        # Handling the case when there are multiple country names
        if country_data:
            # Iterating over the list and inserting each country into the destination database
            for country in country_data:
                # Removing curly braces if present
                country = country.strip('{}')

                # Insert the country information into the destination database
                insert_query = f"INSERT INTO public.Country (name) VALUES ('{country}') ON CONFLICT (name) DO NOTHING;"
                execute_query(insert_query, connection=db_dst)

            # Commit the transaction
            db_dst.commit()

    except Exception as e:
        print(f"Error executing INSERT queries: {e}")
