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

    def check_state(self):
        if self.id is None:
            return False
        return True

    def set_state(self, username, password, seller_id):
        self.username = username
        self.password = password
        self.id = seller_id

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
            return json.loads(response)

    def create_account(self):
        username = input("New Username: ")
        password = input("New Password: ")
        request = {"action": "create_account", "type": "seller", 'body': {"username": username, "password": password}}
        return self.send_request(request)

    def login(self):
        username = input("New Username: ")
        password = input("New Password: ")
        request = {"action": "login", "type": "seller", 'body': {"username": username, "password": password}}
        response = self.send_request(request)
        self.set_state(username, password, response["body"]["seller_id"])
        return response

    def logout(self):
        request = {'actions': 'logout', 'type': 'seller', 'body': {}}
        self.reset_state()
        return self.send_request(request)

    def get_rating(self):
        request = {'action': 'get_rating', 'type': 'seller', 'body': {"seller_id": self.id}}
        response = self.send_request(request)
        print("Rating", response["body"]["rating"])

    def sell(self):
        name = input("Name: ")
        category = input("Category: ")
        keywords = input("Keywords: ")
        condition = input("Condition: ")
        price = input("Price: ")
        quantity = input("Quantity: ")
        request = {'action': 'sell', 'type': 'seller',
                   'body': {'seller_id': self.id,'name': name, 'category': category, 'keywords': keywords,
                            'condition': condition, 'price': price, 'quantity': quantity}}

        return self.send_request(request)

    def update_price(self):
        item = input("Item id: ")
        updated_price = input("Update Price: ")
        request = {'action': 'update_price', 'type': 'seller', 'body': {'username': self.username,
                                                                        'password': self.password,
                                                                        'item_id': item,
                                                                        'price': updated_price}}
        return self.send_request(request)

    def display(self):
        request = {'action': 'get_items_for_seller', 'type': 'seller', 'body': {'username': self.username,
                                                                                'password': self.password,
                                                                                'seller_id': self.id
                                                                                }
                   }
        response = self.send_request(request)
        print(response['body']['body']['items'])

    def remove_item(self):
        item = input("Item id: ")
        quantity = input("Update Quantity: ")
        request = {'action': 'remove_item', 'type': 'seller', 'body': {'item_id': item, 'quantity': quantity}}
        return self.send_request(request)


if __name__ == "__main__":

    seller = SellerClient('127.0.0.1', 1345)
    while True:
        if not seller.check_state():
            print("1. Create Account \n2. Login \n")
            action_number = int(input("Action Number: "))
            print()
            if action_number == 1:
                seller.create_account()
            elif action_number == 2:
                seller.login()
            else:
                print("Give Appropriate Action Number")
                continue
        else:
            print("1. Create Account \n2. Logout \n3. Get Rating \n4. Sell \n5. Change Price \
                  \n6. Remove item \n7. Display \n")
            action_number = int(input("Action Number: "))
            print()
            if action_number == 1:
                seller.create_account()
            elif action_number == 2:
                seller.logout()
            elif action_number == 3:
                seller.get_rating()
            elif action_number == 4:
                seller.sell()
            elif action_number == 5:
                seller.update_price()
            elif action_number == 6:
                seller.remove_item()
            elif action_number == 7:
                seller.display()
