import socket
import psycopg2
import json
from seller.server_seller_helper import *
import sys
import time

class SellerServer:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.operations = 0
        self.start = time.time()
        self.max = 0

        self.server_seller_helper = SellerServerHelper()
        self.create_server_socket()

    def create_server_socket(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.server_host, self.server_port))
        server_socket.listen(1000)
        print("Server Running and Accepting Client Request")

        try:
            while True:
                client_socket, client_address = server_socket.accept()
                print(f"Accepted connection from {client_address}")
                self.handle_client_request(client_socket)
        except KeyboardInterrupt:
            print("\nCtrl+C pressed. Shutting down.")
            server_socket.close()
            sys.exit(0)

    def handle_client_request(self, client_socket):
        self.operations += 1
        data = client_socket.recv(1024).decode('utf-8')
        parsed_data = json.loads(data)
        print(f"Received data from client: {data}")
        action = parsed_data['action']
        self.max = max(self.max, self.operations / (time.time() - self.start))

        # return self.choose_and_execute_action(action,client_socket,parsed_data)
        response = self.server_seller_helper.choose_and_execute_action(action, parsed_data)
        print("response", response)
        client_socket.send(json.dumps(response).encode('utf-8'))
        client_socket.close()
        print(self.max)


if __name__ == "__main__":
    server_host = "localhost"
    server_port = 1345

    seller_server = SellerServer(server_host, server_port)
