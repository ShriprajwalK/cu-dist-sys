import socket
import json
import threading
import time
from prettytable import PrettyTable
import requests

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
        self.url = "http://" + str(self.host) + ":" + str(self.port)
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

        headers = {'Content-type': 'application/json'}
        url_path = self.url + request["path"]
        method = request["method"]

        if(method=="get"):
            response = requests.get(url=url_path, data=json.dumps(request), headers=headers)
            print(response.json())
            return response.json()
        if(method=="put"):
            response = requests.put(url=url_path, data=json.dumps(request), headers=headers)
            print(response.json())
            return response.json()
        if(method=="post"):
            response = requests.post(url=url_path, data=json.dumps(request), headers=headers)
            print(response.json())
            return response.json()
        if(method=="delete"):
            response = requests.delete(url=url_path, data=json.dumps(request), headers=headers)
            print(response.json())
            return response.json()

    def create_account(self):
        username = input("New Username: ")
        password = input("New Password: ")
        request = {"path": "/create_account", "method": "put", 'body': {"username": username, "password": password}}
        response = self.send_request(request)

        if 'error' in response:
            print("Account Not Created : ", response["error"], "\n")
        else:
            print(response['message'])

    def login(self):
        username = 'asdf' #input("New Username: ")
        password = 'asdf' # input("New Password: ")
        request = {"path": "/login", "method": "get", 'body': {"username": username, "password": password}}
        response = self.send_request(request)

        if 'error' in response:
            print("Login Unsuccessful : ", response["error"], "\n")
        else:
            self.set_state(username, password, response["seller_id"], response["session_id"])
            print(response['message'])

        return response

    def logout(self):
        request = {'actions': '/logout', "method": "get", 'body': {}}
        self.reset_state()
        return self.send_request(request)

    def get_rating(self):
        request = {"path": "/get_rating", "method": "get", 'body': {'seller_id': self.id}}
        response = self.send_request(request)

        if(response["rating"]==None):
            print("Seller Id does not exist")
        else:
            print("Seller Rating:", response["rating"])

    def sell(self):
        name = input("Name: ")
        category = input("Category: ")
        keywords = input("Keywords: ")
        condition = input("Condition: ")
        price = input("Price: ")
        quantity = input("Quantity: ")
        request = {"path": '/sell', "method": "post",
                   'body': {'seller_id': self.id,'name': name, 'category': category, 'keywords': keywords,
                            'condition': condition, 'price': price, 'quantity': quantity}}

        return self.send_request(request)

    def update_price(self):
        item = input("Item id: ")
        updated_price = input("Update Price: ")
        request = {"path": '/update_price', "method": "post", 'body': {'username': self.username,
                                                                        'password': self.password,
                                                                        'item_id': item,
                                                                        'price': updated_price}}
        return self.send_request(request)

    def display(self):
        request = {"path": '/get_items_for_seller', "method": "get", 'body': {'username': self.username,
                                                                                'password': self.password,
                                                                                'seller_id': self.id
                                                                                }
                   }
        response = self.send_request(request)
        table = PrettyTable(["Name", "Id", "Quantity","Price"])
        for item in response['items']:
            item_name = item['name']
            item_id = item['id']
            quantity = item['quantity']
            price = item['price']
            if quantity!=0:
                table.add_row([item_name, item_id, quantity,price])
        print(table, "\n")

    def remove_item(self):
        item = input("Item id: ")
        quantity = input("Update Quantity: ")
        request = {"path": '/remove_item', "method": "delete", 'body': {'item_id': item, 'quantity': quantity}}
        return self.send_request(request)


if __name__ == "__main__":
    #seller = SellerClient('34.132.91.142', 1235)
    seller = SellerClient('localhost', 1235)
    ## benchmark
    login_times = []
    for i in range(10):
        start = time.time()
        seller.login()
        login_times.append(time.time()-start)

    rating_times = []
    for i in range(10):

        start = time.time()
        seller.get_rating()
        rating_times.append(time.time()-start)
    print("LOGIN:", sum(login_times) / len(login_times))
    print("RATING:", sum(rating_times) / len(rating_times))
    ## benchmark end

    # warner_thread = threading.Thread(target=warn_or_logout, daemon=True, args=(seller,))
    # warner_thread.start()
    # while True:
    #     if not seller.check_state():
    #         print("1. Create Account \n2. Login \n")
    #         action_number = int(input("Action Number: "))
    #         print()
    #         if action_number == 1:
    #             seller.create_account()
    #         elif action_number == 2:
    #             seller.login()
    #         else:
    #             print("Give Appropriate Action Number")
    #             continue
    #     else:
    #         print("1. Create Account \n2. Logout \n3. Get Rating \n4. Sell \n5. Change Price \
    #               \n6. Remove item \n7. Display \n")
    #
    #         action_number = int(input("Action Number: "))
    #
    #         print()
    #         if action_number == 1:
    #             seller.create_account()
    #         elif action_number == 2:
    #             seller.logout()
    #         elif action_number == 3:
    #             seller.get_rating()
    #         elif action_number == 4:
    #             seller.sell()
    #         elif action_number == 5:
    #             seller.update_price()
    #         elif action_number == 6:
    #             seller.remove_item()
    #         elif action_number == 7:
    #             seller.display()
