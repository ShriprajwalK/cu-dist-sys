import socket
import psycopg2

class BuyerServer:
    def __init__(self, server_host, server_port):
        self.host = server_host
        self.port = server_port
        self._execute_sql_script()
        
        self._create_server_socket(server_host, server_port)

    def execute_sql_script(self):
        conn = psycopg2.connect(host = "localhost",dbname = "postres", password = "daksh1999",port = "5432")
        cursor = conn.cursor()

        with open("init_customer.sql", 'r') as sql_file:
            sql_script = sql_file.read()
            cursor.executescript(sql_script)

        conn.commit()
        print("SQL script executed successfully.")

        conn.commit()
        conn.close()

    def create_server_socket(self, server_host, server_port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((server_host, server_port))
        server_socket.listen(1000)

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")
            self._handle_client_request(client_socket)

    def handle_client_request(self, client_socket):
        data = client_socket.recv(1024)
        print(f"Received data from client: {data}")
        client_socket.close()

if __name__ == "__main__":
    server_host = "localhost"
    server_port = 8000

    buyer_server = BuyerServer(server_host, server_port)