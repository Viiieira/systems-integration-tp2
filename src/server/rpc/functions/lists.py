from functions.execute_query import execute_query

# print("\t4 - List All Wines belonging to a country")
def list_wines_country(country):
    wines = []
    try:
        query = f"""
                SELECT
                    unnest(xpath('/WineReviews/Countries/Country[@name="{country}"]/Provinces/Province/Wines/Wine/@name', xml))::text AS wine_name
                FROM public.imported_documents;
                """

        results = execute_query(query)

        for wine in results:
            wines.append(wine)
        return wines
    except Exception as e:
        print(f"Error executing query: {e}")
        return wines

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
                    unnest(xpath('/WineReviews/Countries/Country/Provinces/Province[@id=//WineReviews/Wineries/Winery/@province_ref]/@name', xml))::text AS province_name,
                    unnest(xpath('/WineReviews/Wineries/Winery/@name', xml))::text AS winery_name
                FROM public.imported_documents
                ORDER BY province_name, winery_name;
                """

        results = execute_query(query)

        wineries_per_province = []
        # Extracting and returning the wineries grouped by province
        for winery_data in results:
            province = winery_data[0].strip('"') if winery_data[0] is not None else ""
            winery = winery_data[1].strip('"')

            # Add winery to the list with its associated province
            wineries_per_province.append({"province": province, "winery": winery})

        return wineries_per_province

    except Exception as e:
        print(f"Error executing query: {e}")
        return []

# print("\t7 - List Wineries ordered by Name ")
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