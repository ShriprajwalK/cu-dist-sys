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
        request = {"action": "get_seller_id", 'body': {"username": username, "password": password}}
        response = self.send_request(request)
        seller_id = response["body"]["seller_id"]
        return seller_id

    def create_seller(self, username, password):
        request = {"action": "create_seller", 'body': {"username": username, "password": password}}
        response = self.send_request(request)
        seller_created = response["body"]["is_created"]
        return seller_created

    def get_all_items(self):
        request = {"action": "get_all_items", 'body': {}}
        response = self.send_request(request)
        items = response["body"]["items"]
        return items

    def get_seller_rating_by_id(self, seller_id):
        request = {"action": "get_seller_rating", 'body': {"seller_id": seller_id}}
        response = self.send_request(request)
        rating = response["body"]["rating"]
        return rating

    def sell_item(self, seller, name, category, keywords, condition, price, quantity):
        request = {"action": "sell_item", "body": {"seller_id": seller, "name": name, "category": category,
                                                   "keywords": keywords, "condition": condition, "price": price,
                                                   "quantity": quantity}}
        response = self.send_request(request)
        return response

    def update_price(self, item_id, price):
        request = {"action": "update_price", "body": {'item_id': item_id, 'price': price}}
        response = self.send_request(request)
        return response

    def remove_item(self, item_id, quantity):
        request = {"action": "remove_item", "body": {'item_id': item_id, 'quantity': quantity}}
        response = self.send_request(request)
        return response

    def get_items_for_seller(self, seller_id):
        request = {"action": "get_items_for_seller", "body": {'seller_id': seller_id}}
        response = self.send_request(request)
        return response
