import socket
import json

class CustomerDatabaseConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send_request(self, request):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(json.dumps(request).encode('utf-8'))
            response = s.recv(1024).decode('utf-8')
            return json.loads(response)
        

    def get_buyer_by_id(self, username, password):
        request = {"action":"get_buyer_id",'body': {"username": username, "password": password}}
        response = self.send_request(request)
        buyer_id = response["body"]["buyer_id"]
        return buyer_id
    
    def create_buyer(self, username, password):
        request = {"action":"create_buyer",'body': {"username": username, "password": password}}
        response = self.send_request(request)
        buyer_created = response["body"]["is_created"]
        return buyer_created
    
    def get_all_items(self):
        request = {"action":"get_all_items",'body': {}}
        response = self.send_request(request)
        items = response["body"]["items"]
        return items
        
