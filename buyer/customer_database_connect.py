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

    def get_purchase_history(self,buyer_id):
        request = {"action":"get_buyer_purchase",'body': {"buyer_id",buyer_id}}
        response = self.send_request(request)
        items = response["body"]["items"]
        return items
    
    def add_to_cart(self,item_id,buyer_id, quantity):
        request = {"action":"create_cart",'body': {"buyer_id": buyer_id, "item_id": item_id, 'quantity': quantity}}
        response = self.send_request(request)
        success = response["body"]["is_created"]
        return success
    
    def delete_cart_by_buyer_id(self, buyer_id):
        request = {"action":"delete_cart_by_buyer_id",'body': {"buyer_id": buyer_id}}
        response = self.send_request(request)
        success = response["body"]["deleted"]
        return success
    
    def remove_cart_item(self, item_id, buyer_id):
        request = {"action":"remove_cart_item",'body': {"buyer_id": buyer_id, "item_id": item_id}}
        response = self.send_request(request)
        success = response["body"]["deleted"]
        return success
    
    def get_cart_item(self, item_id, buyer_id):
        request = {"action":"get_cart_item",'body': {"buyer_id": buyer_id, "item_id": item_id}}
        response = self.send_request(request)
        item = response["body"]["item"]
        return item
    
    def update_cart_item_quantity(self, item_id, buyer_id, quantity):
        request = {"action":"update_cart_item_quantity",'body': {"buyer_id": buyer_id, "item_id": item_id, 'quantity': quantity}}
        response = self.send_request(request)
        success = response["body"]["updated"]
        return success
    
    def get_buyer_cart_items(self, buyer_id):
        request = {"action":"get_buyer_cart_items",'body': {"buyer_id":buyer_id}}
        response = self.send_request(request)
        items = response["body"]["items"]
        return items
        
        
