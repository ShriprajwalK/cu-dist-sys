import socket
import json
from prettytable import PrettyTable
import threading
import time
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


class BuyerClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.url = "http://" + str(self.host) + ":" + str(self.port)
        self.username = None
        self.password = None
        self.id = None
        self.cart = []
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

    def set_state(self, username, password, buyer_id, session_id):
        self.username = username
        self.password = password
        self.id = buyer_id
        self.session_id = session_id

    def send_request(self, request):
        if not request['body']:
            request['body'] = {}
        if self.username and self.password:
            request['body']['username'] = self.username
            request['body']['password'] = self.password
        if self.session_id:
            request['body']['session_id'] = self.session_id
        if self.id:
            request['body']['buyer_id'] = self.id

        headers = {'Content-type': 'application/json'}
        url_path = self.url + request["path"]
        method = request["method"]

        if(method=="get"):
            response = requests.get(url=url_path, data=json.dumps(request), headers=headers)
            return response.json()
        if(method=="put"):
            response = requests.put(url=url_path, data=json.dumps(request), headers=headers)
            return response.json()
        if(method=="post"):
            response = requests.post(url=url_path, data=json.dumps(request), headers=headers)
            return response.json()
        if(method=="delete"):
            response = requests.delete(url=url_path, data=json.dumps(request), headers=headers)
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
        username = input("Username: ")
        password = input("Password: ")
        request = {"path": "/login", "method": "get", 'body': {"username": username, "password": password}}
        response = self.send_request(request)

        if 'error' in response:
            print("Login Unsuccessful : ", response["error"], "\n")
        else:
            self.set_state(username, password, response["buyer_id"], response["session_id"])
            print(response['message'])

        return response

    def logout(self):
        request = {'actions': '/logout', 'method': 'delete', 'body': {}}
        self.reset_state()
        print("Logged Out Successfully \n")

    def search(self):
        item_category = input("Item Category: ")
        keywords = input("Give atleast 5 comma separated keywords: ")
        request = {"path": "/search", "method": "get", 'body': {"item_category": item_category, 'keywords': keywords}}
        response = self.send_request(request)

        table = PrettyTable(["Id","Name", "Quantity", "Price", "Rating"])
        for item in response["items"]:
            item_name = item["item_name"]
            item_id = item["item_id"]
            quantity = item["quantity"]
            price = item["price"]
            rating = item["rating"]
            table.add_row([item_id,item_name, quantity, price, rating])

        print(table, "\n")

    def cart_add(self):
        item_id = int(input("Item Id: "))
        quantity = int(input("Quantity: "))
        request = {"path": "/cart_add", "method": "put", 'body': {"buyer_id": self.id, "item_id": item_id, 'quantity': quantity}}
        response = self.send_request(request)

        if response["add"]:
            print("Item Added to the Cart", "\n")
        else:
            print("Could Not add to the because:", response["message"], "\n")

    def cart_remove(self):
        item_id = int(input("Item Id: "))
        quantity = int(input("Quantity: "))
        request = {"path": "/cart_remove", "method": "delete", 'body': { "buyer_id": self.id, "item_id": item_id, 'quantity': quantity}}
        response = self.send_request(request)
        if response['removed']:
            print("Item Successfully Removed")
        else:
            print("Item Not Found in the Cart")

    def cart_display(self):
        request = {"path": "/cart_display", "method": "get", 'body': {"buyer_id": self.id}}
        response = self.send_request(request)
        items = response["items"]
        if(items == None or len(items) == 0):
            print("No items in the cart")
        else:
            table = PrettyTable(["Name", "Id", "Quantity"])
            for item in items:
                table.add_row([item["item_name"], item["item_id"], item["quantity"]])
            print(table, "\n")

    def cart_clear(self):
        request = {"path": "/cart_clear", "method": "delete", 'body': {"buyer_id":self.id}}
        response = self.send_request(request)
        if(response["cleared"]):
            print("Cart Cleared")
        else:
            print("Cart not Cleared")

    def cart_save(self):
        request = {"path": "/cart_save", "method": "put", 'body': {"buyer_id":self.id}}
        response = self.send_request(request)
        if(response["saved"]):
            print("Cart Saved")
        else:
            print("Cart not Saved")

    def provide_feedback(self):
        request = {"path": "/get_purchase_history", "method": "get", 'body': {"buyer_id":self.id}}
        response = self.send_request(request)
        items = response["items"]
        if(items==None or len(items)==0):
            print("No items purchased")
            return
        else:
            item_rating = {}
            for item in items:
                item_id = item["item_id"]
                input_string  = "Provide Feedback (0 or 1) for item Id " + str(item_id) + ":"
                rating = int(input(input_string))
                item_rating[item_id] = rating

        request = {"path": "/item_rating", "method": "put", 'body': {"rating":item_rating}}
        response = self.send_request(request)

        if(response["success"]==True):
            print("Feedback Stored")
        else:
            print("Feedback Not stored. Try Again")


    def seller_rating(self):
        seller_id = int(input("Seller Id: "))
        request = {"path": "/seller_rating", "method": "get", 'body': {'seller_id': seller_id}}
        response = self.send_request(request)

        if(response["rating"]==None):
            print("Seller Id does not exist")
        else:
            print("Seller Rating:", response["rating"])

    def history(self):
        request = {"path": "/get_purchase_history", "method": "get", 'body': {"buyer_id":self.id}}
        response = self.send_request(request)
        items = response["items"]
        if(items==None or len(items)==0):
            print("No items purchased")
            return
        else:
            table = PrettyTable(["Name", "Id", "Quantity"])
            for item in response["items"]:
                item_name = item["item_name"]
                item_id = item["item_id"]
                quantity = item["quantity"]
                table.add_row([item_name, item_id, quantity])
            print(table, "\n")

    def make_purchase(self):
        request = {"path": '/purchase', "method": "post", 'body': {}}
        response = self.send_request(request)

        if response["status"] == 'Yes':
            print("Purchase Not made")
        else:
            print("Purchase Made Successfully")


if __name__ == "__main__":
    buyer = BuyerClient('127.0.0.1', 1234)
    warner_thread = threading.Thread(target=warn_or_logout, daemon=True, args=(buyer,))
    warner_thread.start()
    while True:
        if not buyer.check_state():
            print("1. Create Account \n2. Login \n")
            action_number = int(input("Action Number: "))
            print()
            if action_number == 1:
                buyer.create_account()
            elif action_number == 2:
                buyer.login()
            else:
                print("Give Appropriate Action Number")
                continue
        else:
            print("1. Create Account \n2. Logout \n3. Search Items \n4. Add Items to Cart \n5. Remove Item From Cart \
                  \n6. Display Cart \n7. Clear the Cart \n8. Save the Cart \n9. Provide Item Feedback \n10. Display Seller Rating \
                  \n11. Display Buyer Purchase History \n12. Purchase the Items\n")
            action_number = int(input("Action Number: "))
            print()
            if action_number == 1:
                buyer.create_account()
            elif action_number == 2:
                buyer.logout()
            elif action_number == 3:
                buyer.search()
            elif action_number == 4:
                buyer.cart_add()
            elif action_number == 5:
                buyer.cart_remove()
            elif action_number == 6:
                buyer.cart_display()
            elif action_number == 7:
                buyer.cart_clear()
            elif action_number == 8:
                buyer.cart_save()
            elif action_number == 9:
                buyer.provide_feedback()
            elif action_number == 10:
                buyer.seller_rating()
            elif action_number == 11:
                buyer.history()
            elif action_number == 12:
                buyer.make_purchase()
