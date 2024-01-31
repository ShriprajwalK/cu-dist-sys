import socket
import json


class SellerClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.username = None
        self.password = None
        self.id = None

    def reset_state(self):
        self.username = None
        self.password = None
        self.id = None

    def set_state(self, state):
        self.username = state['username']
        self.password = state['password']
        self.id = state['buyer_id']

    def send_request(self, request):
        if not request['body']:
            request['body'] = {}
        if self.username and self.password:
            request['body']['username'] = self.username
            request['body']['password'] = self.password

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(json.dumps(request).encode('utf-8'))
            server_response = s.recv(1024).decode('utf-8')
            return server_response

    def create_account(self, username, password):
        request = {"action": "create_account", "type": "seller", 'body': {"username": username, "password": password}}
        return self.send_request(request)

    def login(self, username, password):
        request = {"action": "login", "type": "seller", 'body': {"username": username, "password": password}}
        response = self.send_request(request)
        self.set_state(response)
        return response

    def logout(self):
        request = {'actions': 'logout', 'type': 'seller', 'body': {}}
        self.reset_state()
        return self.send_request(request)

    def get_rating(self):
        request = {'action': 'rating', 'type': 'seller', 'body': {}}
        return self.send_request(request)

    def sell(self, name, category, keywords, condition, price, quantity):
        request = {'action': 'sell', 'type': 'seller',
                   'body': {'name': name, 'category': category, 'keywords': keywords,
                            'condition': condition, 'price': price, 'quantity': quantity}}

        return self.send_request(request)

    def change_price(self, item, price):
        request = {'action': 'change_price', 'type': 'seller', 'body': {'item': item, 'price': price}}
        return self.send_request(request)

    def display(self):
        request = {'action': 'display', 'type': 'seller', 'body': {}}
        return self.send_request(request)

    def remove_item(self, item, quantity):
        request = {'action': 'display', 'type': 'seller', 'body': {'item': item, 'quantity': quantity}}
        return self.send_request(request)


if __name__ == "__main__":
    seller = SellerClient('127.0.0.1', 1234)
    response = seller.create_account('seller1', 'securepass')
    print(response)
    response = seller.login('seller1', 'securepass')
    print(response)
