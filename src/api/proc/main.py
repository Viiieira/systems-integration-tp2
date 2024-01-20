import sys
import xmlrpc.client
from flask import Flask,jsonify
from flask_cors import CORS

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
CORS(app)

server = xmlrpc.client.ServerProxy('http://rpc-server:9000')

# 6 - Get Wineries Grouped by Province
@app.route('/api/province/groupedByWinery')
def api_list_wineries_per_province():
    try:
        provinces = server.list_wineries_per_province()
        response_data = {"provinces": provinces}

        return jsonify(response_data)
    except Exception as e:
        error_message = f"Error calling 'api_list_wineries_per_province': {e}"
        return jsonify({"error": error_message}), 500

# 7 - Get Wineries Ordered By Name
@app.route('/api/winery/getByName', methods=['GET'])
def api_list_wineries_ord_name():
    try:
        wineries = server.list_wineries_ord_name()
        response_data = {"wineries": wineries}

        return jsonify(response_data)

    except Exception as e:
        error_message = f"Error calling 'list_wineries_ord_name': {e}"
        return jsonify({"error": error_message}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT, debug=True)
