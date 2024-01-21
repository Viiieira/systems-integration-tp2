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


@app.route('/api/markers', methods=['GET'])
def get_markers():
    args = request.args

    # Query to retrieve markers for wines with provinces inside the specified box
    query = """
        SELECT
            jsonb_build_object(
                'type', 'feature',
                'geometry', jsonb_build_object(
                    'type', 'Point',
            "       'geometry', st_asgeojson(coords)::jsonb,"
            "       'properties', to_jsonb(marker_data.*) - 'geom'"
                ),
                'properties', jsonb_build_object(
                    'id', wine.id,
                    'name', wine.name,
                    'points', wine.points,
                    'price', wine.price,
                    'winery', wine.winery,
                )
            ) AS marker
        FROM (
            SELECT
                w.id,
                w.name,
                w.country,
                w.position,
                w.imgUrl,
                w.number,
                ST_X(p.coords) AS province_coords[0],
                ST_Y(p.coords) AS province_coords[1]
            FROM wine w
            INNER JOIN province p ON w.id_province = p.id
            WHERE ST_Within(p.coords, ST_MakeEnvelope(%s, %s, %s, %s, 4326))
        ) AS wine
    """

    # Execute the query with the bounding box parameters
    markers = execute_query(
        query,
        [args['neLng'], args['neLat'], args['swLng'], args['swLat']],
        fetchall=True
    )

    return jsonify(markers), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
