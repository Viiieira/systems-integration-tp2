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
def list_wines_amount_points(operator, points):
    wines = []
    try:
        query = f"""
                SELECT unnest(xpath('/WineReviews/Countries/Country/Provinces/Province/Wines/Wine[@points {operator} {points}]/@name', xml))::text AS wine_name
                FROM public.imported_documents;
                """

        results = execute_query(query)

        for wine in results:
            wines.append(wine)
        return wines
    except Exception as e:
        print(f"Error executing query: {e}")
        return wines
    
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
def list_avg_points_wines_province(province):
    average_points = 0
    try:
        query = f"""
            SELECT AVG(points::numeric) AS average_points
            FROM (
                SELECT unnest(xpath('/WineReviews/Countries/Country/Provinces/Province[@name = "{province}"]/Wines/Wine/@points', xml))::text AS points
                FROM public.imported_documents
                WHERE xpath('/WineReviews/Countries/Country/Provinces/Province/@name', xml) IS NOT NULL
            ) AS subquery;
            """
        
        results = execute_query(query)

        average_points = float(results[0][0]) if results else None

        return average_points
    except Exception as e:
        print(f"Error executing query: {e}")
        return average_points
    
def list_countries():
    countries = []
    try:
        # Construct the XPath query to get all wineries ordered by name
        query = """
                SELECT 
                    unnest(xpath('/WineReviews/Countries/Country/@name', xml))::text AS country_name
                FROM public.imported_documents;
                """

        results = execute_query(query)

        for country in results:
            countries.append(country)
        return countries
    except Exception as e:
        print(f"Error executing query: {e}")
        return countries