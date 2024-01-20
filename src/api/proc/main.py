import sys
import xmlrpc.client
from flask import Flask,jsonify
from flask_cors import CORS

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
CORS(app)

server = xmlrpc.client.ServerProxy('http://rpc-server:9000')
# Get Wineries Ordered By Name
@app.route('/api/wineries/ordered_by_name', methods=['GET'])
def api_list_wineries_ord_name():
    try:
        wineries = server.list_wineries_ord_name()
        response_data = {"wineries": wineries}

        return jsonify(response_data)

    except Exception as e:
        error_message = f"Error calling 'list_wineries_ord_name': {e}"
        return jsonify({"error": error_message}), 500

@app.route('/api/helloworld', methods=['GET'])
def api_hello_world():
    try:
        result = server.hello_world()
        response_data = {"message": result}
      
        return jsonify(response_data)

    except Exception as e:
        error_message = f"Error calling 'hello_world': {e}"
        return jsonify({"error": error_message}), 500

@app.route('/api/best_players', methods=['GET'])
def get_best_players():
    return [{
        "id": "7674fe6a-6c8d-47b3-9a1f-18637771e23b",
        "name": "Ronaldo",
        "country": "Portugal",
        "position": "Striker",
        "imgUrl": "https://cdn-icons-png.flaticon.com/512/805/805401.png",
        "number": 7
    }]


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT, debug=True)
