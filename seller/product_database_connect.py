import socket
import json

class ProductDatabaseConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send_request(self, request):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(json.dumps(request).encode('utf-8'))
            response = s.recv(1024).decode('utf-8')
            return json.loads(response)
        

    def get_seller_by_id(self, username, password):
        request = {"action":"get_seller_id",'body': {"username": username, "password": password}}
        response = self.send_request(request)
        seller_id = response["body"]["seller_id"]
        return seller_id
    
    def create_seller(self, username, password):
        request = {"action":"create_seller",'body': {"username": username, "password": password}}
        response = self.send_request(request)
        seller_created = response["body"]["is_created"]
        return seller_created
    
    def get_all_items(self):
        request = {"action":"get_all_items",'body': {}}
        response = self.send_request(request)
        items = response["body"]["items"]
        return items
        
