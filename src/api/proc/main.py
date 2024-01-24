import sys
import xmlrpc.client
from flask import Flask,jsonify,request
from flask_cors import CORS

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
CORS(app)

server = xmlrpc.client.ServerProxy('http://rpc-server:9000')

# http://localhost:20004/api/wine
@app.route('/api/wine')
def get_wines_country():
    try:
        # Extracting country from the query parameters in the URL
        country = request.args.get("country")

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

# http://localhost:20004/api/wine/getByPoints
@app.route('/api/wine/getByPoints')
def get_wines_amount_points():
    try:
        operator_mapping = {
            "greater_than": ">",
            "less_than": "<",
            "equal_to": "=",
            "greater_than_or_equal": ">=",
            "less_than_or_equal": "<=",
            "not_equal": "!=",
        }

        operator = request.args.get("operator")
        points = request.args.get("points")

        if not operator:
            return jsonify({"error": "operator parameter is missing or empty"}), 400
        if not points:
            return jsonify({"error": "points parameter is missing or empty"}), 400

        if operator not in operator_mapping:
            return jsonify({"error": "Invalid operator"}), 400

        actual_operator = operator_mapping[operator]
        wines = server.list_wines_amount_points(actual_operator, points)

        if wines is not None:
            response_data = {"wines": wines}
            return jsonify(response_data)
        else:
            return jsonify({"error": f"No wines were found."}), 404

    except Exception as e:
        error_message = f"Error calling 'get_wines_amount_points': {e}"
        return jsonify({"error": error_message}), 500
        

# http://localhost:20004/api/winery/province
@app.route('/api/winery/province')
def get_wineries_per_province():
    try:
        provinces = server.list_wineries_per_province()
        response_data = {"provinces": provinces}

        return jsonify(response_data)
    except Exception as e:
        error_message = f"Error calling 'api_list_wineries_per_province': {e}"
        return jsonify({"error": error_message}), 500

# http://localhost:20004/api/winery
@app.route('/api/winery', methods=['GET'])
def get_wineries_ord_name():
    try:
        wineries = server.list_wineries_ord_name()
        response_data = {"wineries": wineries}

        return jsonify(response_data)

    except Exception as e:
        error_message = f"Error calling 'list_wineries_ord_name': {e}"
        return jsonify({"error": error_message}), 500
    
# http://localhost:20004/api/province/wine/avg_points
@app.route('/api/province/wine/avg_points')
def get_avg_points_province():
    try:
        province = request.args.get("province")
 
        if not province:
            return jsonify({"error": "province parameter is missing or empty"}), 400
            
        avg_points = server.list_avg_points_wines_province(province)
        
        if avg_points is not 0:
            response_data = {"avg_points": avg_points}
            return jsonify(response_data)
        else:
            return jsonify({"error": f"The province '{province}' was not found"}), 404

    except Exception as e:
        error_message = f"Error calling 'get_avg_points_province': {e}"
        return jsonify({"error": error_message}), 500
    
# http://localhost:20004/api/country
@app.route('/api/country', methods=['GET'])
def get_countries():
    try:
        countries = server.list_countries()
        response_data = {"countries": countries}

        return jsonify(response_data)

    except Exception as e:
        error_message = f"Error calling 'get_countries': {e}"
        return jsonify({"error": error_message}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT, debug=True)
