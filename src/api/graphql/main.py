import sys
import psycopg2
import uuid

from flask import Flask, request, jsonify
import magql
from flask_magql import MagqlExtension

app = Flask(__name__)
app.config["DEBUG"] = True

DATABASE_URL = "postgresql://is:is@db-rel:5432/is"

schema = magql.Schema()

# 4 - List All Wines belonging to a country
@schema.query.field("winesByCountry", "[Wine]")
def resolve_wines_by_country(parent, info, country_name: str):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    try:
        # Fetch the country from the database
        cursor.execute("SELECT id FROM country WHERE name = %s", (country_name,))
        country_id = cursor.fetchone()

        if not country_id:
            return []

        # Fetch all wines belonging to the country
        cursor.execute(
            """
            SELECT w.id, w.name, w.points, w.price, w.variety
            FROM wine w
            JOIN province p ON w.id_province = p.id
            WHERE p.id_country = %s
            """,
            (country_id,)
        )
        wines_data = cursor.fetchall()

        # Convert the result to a list of dictionaries
        wines = [
            {
                "id": wine[0],
                "name": wine[1],
                "points": wine[2],
                "price": float(wine[3]),
                "variety": wine[4],
            }
            for wine in wines_data
        ]

        return wines

    finally:
        cursor.close()
        conn.close()


# 5 - List All Wines that match an input amount of points
@schema.query.field("winesByPoints", "[Wine]")
def resolve_wines_by_points(parent, info, points: int):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    try:
        # Fetch wines by points
        cursor.execute(
            """
            SELECT id, name, points, price, variety
            FROM wine
            WHERE points = %s
            """,
            (points,)
        )
        wines_data = cursor.fetchall()

        # Convert the result to a list of dictionaries
        wines = [
            {
                "id": wine[0],
                "name": wine[1],
                "points": wine[2],
                "price": float(wine[3]),
                "variety": wine[4],
            }
            for wine in wines_data
        ]

        return wines

    finally:
        cursor.close()
        conn.close()

# 7 - Get Wineries Ordered By Name
@schema.query.field("wineriesOrderedByName", "[Winery]")
def resolve_wineries_ordered_by_name(parent, info):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    try:
        # Fetch wineries ordered by name
        cursor.execute(
            """
            SELECT id, name
            FROM winery
            ORDER BY name
            """
        )
        wineries_data = cursor.fetchall()

        # Convert the result to a list of dictionaries
        wineries = [
            {
                "id": winery[0],
                "name": winery[1],
            }
            for winery in wineries_data
        ]

        return wineries

    finally:
        cursor.close()
        conn.close()

# 8 - Get Average Points of Wines for a Province
@schema.query.field("averagePointsByProvince", "Float")
def resolve_average_points_by_province(parent, info, province_name: str):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    try:
        # Fetch the province from the database
        cursor.execute("SELECT id FROM province WHERE name = %s", (province_name,))
        province_id = cursor.fetchone()

        if not province_id:
            return None

        # Fetch the average points of wines in the province
        cursor.execute(
            """
            SELECT AVG(points) 
            FROM wine
            WHERE id_province = %s
            """,
            (province_id,)
        )
        average_points = cursor.fetchone()[0]

        return float(average_points) if average_points is not None else None

    finally:
        cursor.close()
        conn.close()

magql_ext = MagqlExtension(schema)
magql_ext.init_app(app)

@app.route('/graphql', methods=['POST'])
def graphql():
    # Access the GraphQL query from the request
    graphql_query = request.get_json().get("query", "")
    
    # Execute the GraphQL query
    result = magql_ext.execute(graphql_query)
    
    return result

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=sys.argv[1])
