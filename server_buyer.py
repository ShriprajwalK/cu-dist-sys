import socket
import psycopg2
from customer_database import *
import json

class BuyerServer:
    def __init__(self, server_host, server_port,db_connection):
        self.server_host = server_host
        self.server_port = server_port
        self.db_connection = db_connection
        self.sql_init()
        
        self.create_server_socket()

    def sql_init(self):

        with self.db_connection.cursor() as cursor:
            cursor.execute(open("init_customer.sql", "r").read())

        self.db_connection.commit()
        print("SQL script executed successfully.")

    def create_server_socket(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.server_host, self.server_port))
        server_socket.listen(1000)
        print("Server Running and Accepting Client Request")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")
            self.handle_client_request(client_socket)

    def handle_client_request(self, client_socket):
        data = client_socket.recv(1024).decode('utf-8')
        parsed_data = json.loads(data)
        print(f"Received data from client: {data}")
        action = parsed_data['action']

        return self.choose_and_execute_action(action,client_socket,parsed_data)
        

    def choose_and_execute_action(self,action,client_socket,data):
        response = {"action": action, "type": "buyer"}
        if(action=="create_account"):
            username = data["body"]["username"]
            password = data["body"]["password"]
            try:
                create_buyer(self.db_connection, username,password)
                response['body']= {"is_created":True}
            except Exception as e:
                response['body'] = {"is_created":False, "error":str(e)}

        if(action=="login"):
            username = data["body"]["username"]
            password = data["body"]["password"]
            try:
                buyer_id = check_buyer_credentials(self.db_connection, username,password)

                if(buyer_id!=None):
                    response['body'] = {"login":True,"buyer_id" : buyer_id}
                else:
                    response['body'] = {"login":False, "error":"Username/Password does not exist"}
            except Exception as e:
                response['body'] = {"login":False, "error":str(e)}
                
        client_socket.send(json.dumps(response).encode('utf-8'))
        client_socket.close()
        return response        



if __name__ == "__main__":
    server_host = "localhost"
    server_port = 1234  
    db_connection = connect()

    buyer_server = BuyerServer(server_host, server_port,db_connection)