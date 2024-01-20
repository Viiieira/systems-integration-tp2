from functions.execute_query import execute_query

# print("\t4 - List All Wines belonging to a country")
def list_wines_country(country):
    try:
        # country = input("Enter a country (e.g., Spain): ")

        query = f"SELECT xpath('/WineReviews/Countries/Country[@name=\"{country}\"]/Wines/Wine/@name', xml) AS wine_names FROM public.imported_documents;"

        results = execute_query(query)

        if len(results) > 0:
            # Extracting the wine names from the result
            wines_str = results[0][0]

            # Handling the case when there are multiple wine names
            if wines_str:
                wines_list = wines_str.split(',')

                # Iterating over the list and printing each wine name
                for wine in wines_list:
                    print(f"> {wine.strip()}")
            else:
                print(f"There are no wines for the country: {country}")
        else:
            print(f"There are no wines for the country: {country}")

    except Exception as e:
        print(f"Error executing query: {e}")

# print("\t5 - List All Wines that match an input amount of points")
def list_wines_amoint_points(operator, points):
    query = f"SELECT xpath('/WineReviews/Countries/Country[Wines/Wine[@points {operator} {points}]]/Wines/Wine/@name', xml)::text AS wine_name " \
            f"FROM public.imported_documents;"

    try:
        results = execute_query(query)

        if len(results) > 0:
            # Extracting the wines names from the result
            names_str = results[0][0]

            # Removing curly braces and quotes
            names_string = names_str.replace('{', '').replace('}', '').replace('"', '')

            # Splitting the string into a list of countries
            names_list = names_string.split(',')

            # Iterating over the list and printing each country
            for name in names_list:
                print(f"> {name.strip()}")
        else:
            print("No wines match the criteria.")

    except Exception as e:
        print(f"Error executing query: {e}")
    pass

# print("\t6 - List Wineries grouped by Province")
def list_wineries_per_province():
    try:
        # Construct the XPath query to get all wineries grouped by province
        query = """
                SELECT 
                    unnest(xpath('/WineReviews/Wineries/Winery/@winery', xml))::text AS winery_name,
                    unnest(xpath('/WineReviews/Wineries/Winery/@province', xml))::text AS province
                FROM public.imported_documents
                ORDER BY province, winery_name;
                """

        results = execute_query(query)

        if len(results) > 0:
            # Extracting and printing the wineries grouped by province
            current_province = None
            for winery_data in results:
                winery_name = winery_data[0].strip('"')
                province = winery_data[1].strip('"')

                # Print province header when it changes
                if province != current_province:
                    print(f"Province: {province}")
                    current_province = province

                print(f"> Winery Name: {winery_name}")
        else:
            print("No wineries found.")

    except Exception as e:
        print(f"Error executing query: {e}")

# print("\t7 - List Wineries ordered by Name ")
# TODO: WIP, query doesnt return anything
def list_wineries_ord_name():
    try:
        # Construct the XPath query to get all wineries ordered by name
        query = """
                SELECT 
                    unnest(xpath('/WineReviews/Wineries/Winery/@name', xml))::text AS winery_name
                FROM public.imported_documents
                ORDER BY winery_name;
                """

        results = execute_query(query)
        print(f"Results: {results}")

        wineries = []

        if len(results) > 0:
            # Extracting and printing the wineries ordered by name
            for winery_data in results:
                winery_name = winery_data[0].strip('"')
                wineries.append(winery_name)
        else:
            print("No wineries found.")

        return wineries

    except Exception as e:
        print(f"Error executing query: {e}")
        return []

# print("\t8 - List Average Points of Wines of a Province")
def list_avg_points_wines_province():
    try:
        country = input("Enter a country (e.g., Italy): ")

        # Construct the XPath query to get wines from the input country and their respective tasters
        query = f"""
                SELECT 
                    unnest(xpath('/WineReviews/Countries/Country[@name="{country}"]/Wines/Wine/@name', xml))::text AS wine_name,
                    unnest(xpath('/WineReviews/Countries/Country[@name="{country}"]/Wines/Wine/@taster_ref', xml))::text AS taster_ref,
                    xpath('/WineReviews/Tasters/Taster[@id=unnest(xpath('/WineReviews/Countries/Country[@name="{country}"]/Wines/Wine/@taster_ref', xml))::text)]/@taster_name', xml)::text AS taster_name,
                    xpath('/WineReviews/Tasters/Taster[@id=unnest(xpath('/WineReviews/Countries/Country[@name="{country}"]/Wines/Wine/@taster_ref', xml))::text)]/@taster_twitter_handle', xml)::text AS taster_twitter_handle
                FROM public.imported_documents
                WHERE xpath('/WineReviews/Countries/Country/@name', xml) = '{country}';
                """

        results = execute_query(query)

        if len(results) > 0:
            # Extracting and printing the wines and their respective tasters
            for wine_data in results:
                wine_name = wine_data[0].strip('"')
                taster_ref = wine_data[1].strip('"')
                taster_name = wine_data[2].strip('"')
                taster_twitter_handle = wine_data[3].strip('"')

                print(f"> Wine Name: {wine_name}")
                print(f"  Taster Name: {taster_name}, Taster Twitter Handle: {taster_twitter_handle}")
        else:
            print(f"No wines found for the country: {country}")

    except Exception as e:
        print(f"Error executing query: {e}")

def hello_world():
    return "Hello World"