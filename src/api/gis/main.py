import sys
import psycopg2
from psycopg2.extras import RealDictCursor

from flask import Flask, request, jsonify

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
app.config["DEBUG"] = True

DB_PARAMS = {
    "dbname": "is",
    "user": "is",
    "password": "is",
    "host": "db-rel",
    "port": "5432",
}

def execute_query(query, params=None, fetchall=True):
    connection = psycopg2.connect(**DB_PARAMS)
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute(query, params)
        result = cursor.fetchall() if fetchall else cursor.fetchone()
        return result

    finally:
        cursor.close()
        connection.close()


@app.route('/get_provinces', methods=['GET'])
def get_provinces():
    try:
        limit = int(request.args.get('limit', 70))

        # Use execute_query to fetch provinces
        query = f"SELECT * FROM provinces LIMIT %s"
        provinces = execute_query(query, (limit,), fetchall=True)

        if provinces is None:
            # Handle the case where data retrieval was unsuccessful
            return jsonify({"error": "Failed to retrieve provinces data"}), 500

        result = []
        for province in provinces:
            result.append({
                "id": province.get('id'),
                "name": province.get('name'),
                "coordinates": province.get('coords')
                # Add other province attributes as needed
            })

        return jsonify(result), 200

    except Exception as e:
        # Handle other exceptions
        return jsonify({"error": str(e)}), 500

@app.route('/update_province_coords', methods=['PATCH'])
def update_province_coords():
    try:
        data = request.json
        province_name = data.get('province_name')
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if not province_name or not latitude or not longitude:
            return jsonify({"error": "Missing required data"}), 400

        update_query = f"UPDATE provinces SET coords = ST_SetSRID(ST_MakePoint({longitude}, {latitude}), 4326) WHERE name = '{province_name}'"
        execute_query(update_query)

        return jsonify({"message": "Coordinates updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/get_plain_coordinates', methods=['GET'])
def get_plain_coordinates():
    try:
        # Use request.args to get the 'country_id' query parameter
        country_id = request.args.get('id')

        # Check if 'country_id' is provided
        if not country_id:
            return jsonify({"error": "Missing 'id' parameter"}), 400

        # Use parameterized query to avoid SQL injection
        query = "SELECT ST_AsText(coords) FROM provinces WHERE id = %s"

        try:
            # Execute execute_query with the query and parameters
            result = execute_query(query, (country_id,), fetchall=False)

            # Check if result is not None
            if result:
                # Extract coordinates from the result
                text_coordinates = result.get('st_astext') if result else 'N/A'
                if text_coordinates != 'N/A':
                    # Extracting latitude and longitude from the "POINT(lon lat)" format
                    lon_lat_str = text_coordinates.replace('POINT(', '').replace(')', '')
                    lon, lat = map(float, lon_lat_str.split())
                    return jsonify({"longitude": lon, "latitude": lat}), 200
                else:
                    return jsonify({"error": "Coordinates not found for the given id"}), 404
            else:
                return jsonify({"error": f"No result found for id {id}"}), 404
        except Exception as e:
            # Handle exceptions related to database operations
            return jsonify({"error": f"Database error: {str(e)}"}), 500

    except Exception as e:
        # Handle other exceptions
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
