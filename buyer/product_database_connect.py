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

    def get_all_items(self):
        request = {"action":"get_all_items",'body': {}}
        response = self.send_request(request)
        items = response["body"]["items"]
        return items
    
    def get_item_by_id(self, item_id):
        request = {"action":"get_item_by_id",'body': {"item_id":item_id}}
        response = self.send_request(request)
        item = response["body"]["item"]
        return item
    
    def update_item_rating(self, item_id,item_rating):
        request = {"action":"update_item_rating",'body': {"item_id":item_id,"item_rating":item_rating}}
        response = self.send_request(request)
        success = response["body"]["success"]
        return success
    
    def get_item_seller_id(self, item_id):
        request = {"action":"get_item_seller_id",'body': {"item_id":item_id}}
        response = self.send_request(request)
        seller_id = response["body"]["seller_id"]
        return seller_id
    
    def update_seller_rating(self, seller_id,item_rating):
        request = {"action":"update_item_rating",'body': {"seller_id":seller_id,"item_rating":item_rating}}
        response = self.send_request(request)
        success = response["body"]["success"]
        return success
    
    def get_item_price(self, item_id):
        request = {"action":"get_item_price",'body': {"item_id":item_id}}
        response = self.send_request(request)
        price = response["body"]["price"]
        return price
    
