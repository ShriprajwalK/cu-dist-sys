import socket
import psycopg2
from ..postgres.customer_database import *
from ..postgres.product_database import *
from ..postgres.postgres_helper import get_db
import json
from .server_buyer_helper import *
import sys


class BuyerServer:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port

        self.customer_db = get_db('customer')
        self.product_db = get_db('product')

        self.server_buyer_helper = BuyerServerHelper(self.customer_db, self.product_db)
        # self.databases_init()
        self.create_server_socket()

    # def databases_init(self):
    #    self.customer_db.database_init("init_customer.sql")
    #    self.product_db.database_init("init_product.sql")

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
        data = client_socket.recv(1024).decode('utf-8')
        parsed_data = json.loads(data)
        print(f"Received data from client: {data}")
        action = parsed_data['action']

        # return self.choose_and_execute_action(action,client_socket,parsed_data)
        response = self.server_buyer_helper.choose_and_execute_action(action, parsed_data)
        print("response", response)
        client_socket.send(json.dumps(response).encode('utf-8'))
        client_socket.close()


if __name__ == "__main__":
    server_host = "localhost"
    server_port = 1234

    buyer_server = BuyerServer(server_host, server_port)
