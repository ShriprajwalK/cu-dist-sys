import socket
import json

class BuyerClient:
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
            response = s.recv(1024).decode('utf-8')
            return response

    def create_account(self, username, password):
        request = {"action": "create_account", "type": "buyer", 'body': { "username": username, "password": password }}
        return self.send_request(request)

    def login(self, username, password):
        request = {"action": "login", "type": "buyer", 'body': { "username": username, "password": password }}
        response = self.send_request(request)
        self.set_state(response)
        return response

    def logout(self):
        request = {'actions': 'logout', 'type': 'buyer', 'body': {}}
        self.reset_state()
        return self.send_request(request)

    def search(self, item, keywords):
        request = {"action": "search", "type": "buyer", 'body': { "category": item, 'keywords': keywords }}
        return self.send_request(request)

    def cart_add(self, item, num):
        request = {"action": "cart_add", "type": "buyer", 'body': { "item": item, 'quantity': num}}
        return self.send_request(request)

    def cart_remove(self, item, num):
        request = {"action": "cart_remove", "type": "buyer", 'body': { "item": item, 'quantity': num}}
        return self.send_request(request)

    def cart_display(self):
        request = {"action": "cart_display", "type": "buyer", 'body': {}}
        return self.send_request(request)

    def cart_clear(self):
        request = {"action": "cart_clear", "type": "buyer", 'body': {}}
        return self.send_request(request)

    def cart_save(self):
        request = {"action": "cart_save", "type": "buyer", 'body': {}}
        return self.send_request(request)

    def provide_feedback(self, item, feedback):
        request = {"action": "feedback", "type": "buyer", 'body': {'item': item, 'feedback': feedback}}
        return self.send_request(request)

    def seller_rating(self, seller_id):
        request = {"action": "seller_rating", "type": "buyer", 'body': {'id': seller_id}}
        return self.send_request(request)

    def history(self):
        request = {"action": "seller_rating", "type": "buyer", 'body': {}}
        return self.send_request(request)

    def make_purchase(self):
        # We will have to implement this anyway to test history, feedback and seller rating.
        request = {"action": 'purchase', 'type': 'buyer', 'body': {}}
        return self.send_request(request)
   


if __name__ == "__main__":
    buyer = BuyerClient('127.0.0.1', 1234)
    response = buyer.create_account('buyer1', 'password123')
    print(response)
    response = buyer.login('buyer1', 'password123')
    print(response)
