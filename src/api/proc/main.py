import sys
import xmlrpc.client
from flask import Flask,jsonify,request
from flask_cors import CORS

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
CORS(app)

server = xmlrpc.client.ServerProxy('http://rpc-server:9000')

# 4 - List All Wines belonging to a country
# TODO - 
@app.route('/api/wines/country')
def get_wines_country():
    try:
        if request.is_json:
            data = request.json

            if "country" not in data:
                return jsonify({"error": "Country parameter is missing in the request JSON"}), 400
            
            country = data.get("country")
        else:
            return jsonify({"error": "Invalid request format. Expected JSON."}), 400

        if not country:
            return jsonify({"error": "Country parameter is missing or empty"}), 400
            
        wines = server.list_wines_country(country)
        
        if wines is not None:
            response_data = {"wines": wines}
            return jsonify(response_data)
        else:
            return jsonify({"error": f"No wines found for country '{country}'"}), 404

    except Exception as e:
        error_message = f"Error calling 'api_list_wines_country': {e}"
        return jsonify({"error": error_message}), 500


# 6 - Get Wineries Grouped by Province
@app.route('/api/province/groupedByWinery')
def get_wineries_per_province():
    try:
        provinces = server.list_wineries_per_province()
        response_data = {"provinces": provinces}

        return jsonify(response_data)
    except Exception as e:
        error_message = f"Error calling 'api_list_wineries_per_province': {e}"
        return jsonify({"error": error_message}), 500

# 7 - Get Wineries Ordered By Name
@app.route('/api/winery/getByName', methods=['GET'])
def get_wineries_ord_name():
    try:
        wineries = server.list_wineries_ord_name()
        response_data = {"wineries": wineries}

        return jsonify(response_data)

    except Exception as e:
        error_message = f"Error calling 'list_wineries_ord_name': {e}"
        return jsonify({"error": error_message}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT, debug=True)
