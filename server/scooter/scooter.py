import socket
import threading
import json
import signal
import os

from flask import jsonify
from gps3 import gps3
from time import time

PORT = 5000
HOST = '127.0.0.1'
MESSAGE_LIMIT = 30_000_000  # 10 MB


class Scooter:
    """
    Hanldes a server using the protocol AACR (Adapted Application Communication and Routing) 
    """

    def __init__(self, host: str = HOST, port: int = PORT, buffer_size: int = MESSAGE_LIMIT) -> None:
        """
        Create the server using the given host and port

        Args:
            host (str, optional): The host address, probably localhost. Defaults to HOST.
            port (int, optional): The port to make communications. Defaults to PORT.
            buffer_size (int, optional): The port to make communications. Defaults to PORT.
        """
        self.host = host
        self.port = port
        self.buffer_size = buffer_size

        # Creates a socket to allow connections
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.gps_socket = gps3.GPSDSocket()
        self.data_stream = gps3.DataStream()
        self.gps_socket.connect()
        self.gps_socket.watch()
        print("[INFO] Server started on {}:{}".format(self.host, self.port))

    def start_server(self) -> None:
        """
        Listens for connections and if one is adquired accepts it and handles it
        """
        while True:
            # Accept any connection incomming
            client_socket, client_address = self.server_socket.accept()
            print("[INFO] Connected to {}:{}".format(client_address[0], client_address[1]))
            # Create a new thread to handle the client request
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def start(self) -> None:
        """
            Intended way to start the server.
        """
        signal.signal(signal.SIGINT, self.exit_handler)
        # Create a thread for the server to run onto
        server_thread = threading.Thread(target=self.start_server)
        server_thread.start()
        while True:
            try:

                pass
            except KeyboardInterrupt:
                break

        print("[INFO] Stopping the server...")
        server_thread.join()
        print("[INFO] Server stopped.")

    def handle_client(self, client_socket: socket.socket) -> None:
        """
        Handles a client request

        Args:
            client_socket (socket.socket): client socket where connection is made
        """
        while True:
            # Gets client's request
            data = self.get_data(client_socket)
            try:
                # Parses the data into JSON
                data_json = json.loads(data.decode())

                # If no data passed or an invalid method passed, return an error
                if not data_json or "method" not in data_json:
                    self.send_response(client_socket, {"errorCode": "400", "error": "Method not found"})
                    break

                # Get the method and the endpoint to be hit, default to /
                requested_method = data_json["method"]
                requested_uri = data_json.get("uri", "/")

                # Python switch xd
                method_functions = {
                    "LOCATION": self.location,
                    "UNLOCK": self.unlock,
                    "LOCK": self.lock,
                }

                # Execute the request in the correct method
                if requested_method in method_functions:
                    self.execute_request(client_socket, method_functions[requested_method])

                break
            except TypeError as e:
                # This means the method called had errors in the parameters passed
                self.send_response(client_socket, {"errorCode": "400", "error": str(e)})
                break
            except Exception as e:
                # Error parsing JSON or any other
                self.send_response(client_socket, {"errorCode": "500", "error": str(e)})
                break

        client_socket.close()
        print("[INFO] Disconnected from client, request succeded")

    def get_data(self, client_socket: socket.socket) -> bytes:
        """
        Gets the data recived from a socket.

        Args:
            client_socket (socket.socket): socket connection to the client

        Returns:
            (bytes): the recovered data from the connection 
        """
        client_socket.settimeout(3)

        try:
            # Retrive request send by the client
            data = client_socket.recv(self.buffer_size)  # Adjust the buffer size as needed
        except socket.timeout:
            data = b''

        return data

    def exit_handler(self, signal, frame) -> None:
        """
        Gracefully closes the program
        """
        print("[INFO] Closing server...")
        os._exit(0)

    def send_response(self, client_socket: socket.socket, response: dict) -> None:
        """
        Sends a JSON response to the client.

        Args:
            client_socket (socket.socket): a socket where the client is connected
            response (dict): a response object. 
        """
        response_json = json.dumps(response)
        client_socket.send(response_json.encode())

    def execute_request(self, client_socket: socket.socket, func) -> None:
        """
        Executes the request asked by the client, using the know methods functions.

        Args:
            func: the "function" client has requested
            client_socket (socket.socket): socket to client connection.
        """
        response = func()
        self.send_response(client_socket, response)

    def location(self):
        start_time = time()
        for new_data in self.gps_socket:
            if new_data:
                lng = self.data_stream.TPV['lon']
                lat = self.data_stream.TPV['lat']
                self.data_stream.unpack(new_data)
                if lng != 'n/a' and lat != 'n/a':
                    return {'lat': lat, 'lng': lng}
                if time() - start_time > 30:
                    return {'error': 'Timeout'}

    def lock(self):
        return {'message': 'Scooter is locked'}

    def unlock(self):
        return {'message': 'Scooter is unlocked'}


if __name__ == '__main__':
    scooter = Scooter(host='192.168.1.108', port=12345)
    scooter.start_server()
