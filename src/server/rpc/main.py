import signal, sys, json

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from functions.execute_query import execute_query
from functions.lists import *

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

if __name__ == "__main__":
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/RPC2',)

    with SimpleXMLRPCServer(('0.0.0.0', PORT), requestHandler=RequestHandler, allow_none=True) as server:
        server.register_introspection_functions()

        def signal_handler(signum, frame):
            print("received signal")
            server.server_close()

            # perform clean up, etc. here...
            print("exiting, gracefully")
            sys.exit(0)

        # signals
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGHUP, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)

        # register functions with print statements
        print("Registering execute_query function...")
        server.register_function(execute_query)

        print("Registering list_wines_country function...")
        server.register_function(list_wines_country)

        print("Registering list_wines_amoint_points function...")
        server.register_function(list_wines_amoint_points)

        print("Registering list_wineries_per_province function...")
        server.register_function(list_wineries_per_province)

        print("Registering list_wineries_ord_name function...")
        server.register_function(list_wineries_ord_name)

        print("Registering list_avg_points_wines_province function...")
        server.register_function(list_avg_points_wines_province)

        print("Registering hello_world test function...")
        server.register_function(hello_world)

        # start the server
        print(f"Starting the RPC Server in port {PORT}...")
        server.serve_forever()
