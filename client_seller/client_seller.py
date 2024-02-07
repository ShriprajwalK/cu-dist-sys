import socket
import json
import threading
import time
from prettytable import PrettyTable

SESSION_WARN = 240
SESSION_TIMEOUT = 300


def warn_or_logout(user):
    print('warning in 4 mins')
    while True:
        if user.active_time:
            if time.time() - user.active_time >= SESSION_TIMEOUT:
                print("SESSION has expired, logging off")
                user.reset_state()
            elif time.time() - user.active_time >= SESSION_WARN:
                print("Please act within 1 min seconds for the session to continue")
        time.sleep(30)


class SellerClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.username = None
        self.password = None
        self.id = None
        self.session_id = None
        self.active_time = None

    def reset_state(self):
        self.username = None
        self.password = None
        self.id = None
        self.session_id = None
        self.active_time = None

    def check_state(self):
        if self.id is None:
            return False
        return True

    def set_state(self, username, password, seller_id, session_id):
        self.username = username
        self.password = password
        self.id = seller_id
        self.session_id = session_id

    def send_request(self, request):
        if not request['body']:
            request['body'] = {}
        if self.username and self.password:
            request['body']['username'] = self.username
            request['body']['password'] = self.password
        if self.session_id:
            request['body']['session_id'] = self.session_id

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(json.dumps(request).encode('utf-8'))
            response = s.recv(1024).decode('utf-8')
            self.active_time = time.time()
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
        self.set_state(username, password, response["body"]["seller_id"], response['body']['session_id'])
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
        table = PrettyTable(["Name", "Id", "Quantity","Price"])
        for item in response['body']['body']['items']:
            item_name = item[6]
            item_id = item[0]
            quantity = item[2]
            price = item[3]
            if quantity!=0:
                table.add_row([item_name, item_id, quantity,price])
        print(table, "\n")

    def remove_item(self):
        item = input("Item id: ")
        quantity = input("Update Quantity: ")
        request = {'action': 'remove_item', 'type': 'seller', 'body': {'item_id': item, 'quantity': quantity}}
        return self.send_request(request)


if __name__ == "__main__":

    seller = SellerClient('127.0.0.1', 1345)
    warner_thread = threading.Thread(target=warn_or_logout, daemon=True, args=(seller,))
    warner_thread.start()
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
