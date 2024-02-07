import socket
import json
from prettytable import PrettyTable
import threading
import time

SESSION_WARN = 24
SESSION_TIMEOUT = 30


def warn_or_logout(user):
    print('warning in 4 mins')
    while True:
        if user.active_time:
            if time.time() - user.active_time >= SESSION_TIMEOUT:
                print("Please act within 60 seconds for the session to continue")
            elif time.time() - user.active_time >= SESSION_WARN:
                print("SESSION has expired, logging off")
                user.reset_state()
        time.sleep(30)


class BuyerClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.username = None
        self.password = None
        self.id = None
        self.cart = []
        self.session_id = None
        self.active_time = None
        self.times = {}

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

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(json.dumps(request).encode('utf-8'))
            response = s.recv(1024).decode('utf-8')
            self.active_time = time.time()
            return json.loads(response)

    def create_account(self):
        username = input("New Username: ")
        password = input("New Password: ")
        request = {"action": "create_account", "type": "buyer", 'body': {"username": username, "password": password}}
        response = self.send_request(request)

        if 'error' in response['body']:
            print("Account Not Created : ", response["body"]["error"], "\n")
        else:
            print(response['body']['message'])

    def login(self):
        start = time.time()
        username = 'asdf' #input("Username: ")
        password = 'asdf' #input("Password: ")
        request = {"action": "login", "type": "buyer", 'body': {"username": username, "password": password}}
        response = self.send_request(request)
        end = time.time()

        if 'login' not in self.times:
            self.times['login'] = [end - start]
        else:
            self.times['login'].append(end - start)
        if 'error' in response['body']:
            print("Login Unsuccessful : ", response["body"]["error"], "\n")
        else:
            self.set_state(username, password, response["body"]["buyer_id"], response["body"]["session_id"])
            print(response['body']['message'])

        return response

    def logout(self):
        request = {'actions': 'logout', 'type': 'buyer', 'body': {}}
        self.reset_state()
        print("Logged Out Successfully \n")

    def search(self):
        item_category = input("Item Category: ")
        keywords = input("Give atleast 5 comma separated keywords: ")
        request = {"action": "search", "type": "buyer", 'body': {"item_category": item_category, 'keywords': keywords}}
        response = self.send_request(request)

        response_body = response["body"]
        table = PrettyTable(["Id", "Quantity", "Price", "Rating"])
        for item in response_body["items"]:
            item_id = item["item_id"]
            quantity = item["quantity"]
            price = item["price"]
            rating = item["rating"]
            table.add_row([item_id, quantity, price, rating])

        print(table, "\n")

    def cart_add(self):
        item_id = int(input("Item Id: "))
        quantity = int(input("Quantity: "))
        request = {"action": "cart_add", "type": "buyer", 'body': {"buyer_id": self.id, "item_id": item_id, 'quantity': quantity}}
        response = self.send_request(request)

        response_body = response["body"]

        if response_body["add"]:
            print("Item Added to the Cart", "\n")
        else:
            print("Could Not add to the because:", response_body["message"], "\n")

    def cart_remove(self):
        item_id = int(input("Item Id: "))
        quantity = int(input("Quantity: "))
        request = {"action": "cart_remove", "type": "buyer", 'body': { "buyer_id": self.id, "item_id": item_id, 'quantity': quantity}}
        response = self.send_request(request)
        response_body = response["body"]
        if response_body['removed']:
            print("Item Successfully Removed")
        else:
            print("Item Not Found in the Cart")

    def cart_display(self):
        start = time.time()
        request = {"action": "cart_display", "type": "buyer", 'body': {"buyer_id": 1}}
        response = self.send_request(request)
        end = time.time()
        if 'display' not in self.times:
            self.times['display'] = [end - start]
        else:
            self.times['display'].append(end - start)
        response_body = response["body"]
        items = response_body["items"] 
        if(len(items)==0 or items== None):
            print("No items in the cart")
        else:
            table = PrettyTable(["Id", "Quantity", "Price"])
            for item in items:
                table.add_row([item["item_id"], item["quantity"], item["price"]])
            print(table, "\n")

    def cart_clear(self):
        request = {"action": "cart_clear", "type": "buyer", 'body': {"buyer_id":self.id}}
        response = self.send_request(request)
        response_body = response["body"]
        if(response_body["cleared"]):
            print("Cart Cleared")
        else:
            print("Cart not Cleared")

    def cart_save(self):
        request = {"action": "cart_save", "type": "buyer", 'body': {"buyer_id":self.id}}
        response = self.send_request(request)
        response_body = response["body"]
        if(response_body["saved"]):
            print("Cart Saved")
        else:
            print("Cart not Saved")

    def provide_feedback(self):
        request = {"action": "get_purchase_history", "type": "buyer", 'body': {"buyer_id":self.id}}
        response = self.send_request(request)
        response_body = response['body']
        items = response_body["items"]
        if(items==None or len(items)==0):
            print("No items purchased")
            return
        else:
            item_rating = {}
            for item in items:
                item_id = item["item_id"]
                rating = int(input("Provide Feedback (0 or 1) for item Id: ",item_id))
                item_rating[item_id] = rating

        request = {"action": "item_rating", "type": "buyer", 'body': {"rating":item_rating}}
        response = self.send_request(request)

        if(response["body"]["success"]==True):
            print("Feedback Stored")
        else:
            print("Feedback Not stored. Try Again")


    def seller_rating(self):
        seller_id = int(input("Seller Id: "))
        request = {"action": "seller_rating", "type": "buyer", 'body': {'seller_id': seller_id}}
        response = self.send_request(request)

        if(response["body"]["rating"]==None):
            print("Seller Id does not exist")
        else:
            print("Seller Rating:", response["body"]["rating"])

    def history(self):
        request = {"action": "get_purchase_history", "type": "buyer", 'body': {"buyer_id":self.id}}
        response = self.send_request(request)
        response_body = response['body']
        items = response_body["items"]
        if(items==None or len(items)==0):
            print("No items purchased")
            return
        else:
            table = PrettyTable(["Id", "Quantity"])
            for item in response_body["items"]:
                item_id = item["item_id"]
                quantity = item["quantity"]
                table.add_row([item_id, quantity])
            print(table, "\n")

    def make_purchase(self):
        #TBD
        # # We will have to implement this anyway to test history, feedback and seller rating.
        request = {"action": 'purchase', 'type': 'buyer', 'body': {}}
        return self.send_request(request)


if __name__ == "__main__":
    buyer = BuyerClient('127.0.0.1', 1234)
    for i in range(1000):
        buyer.login()
        buyer.cart_display()
    print("login:", sum(buyer.times['login']) / len(buyer.times['login']))
    print("display:", sum(buyer.times['display']) / len(buyer.times['display']))
    # warner_thread = threading.Thread(target=warn_or_logout, daemon=True, args=(buyer,))
    # warner_thread.start()
    # while True:
    #     if not buyer.check_state():
    #         print("1. Create Account \n2. Login \n")
    #         action_number = int(input("Action Number: "))
    #         print()
    #         if action_number == 1:
    #             buyer.create_account()
    #         elif action_number == 2:
    #             buyer.login()
    #         else:
    #             print("Give Appropriate Action Number")
    #             continue
    #     else:
    #         print("1. Create Account \n2. Logout \n3. Search Items \n4. Add Items to Cart \n5. Remove Item From Cart \
    #               \n6. Display Cart \n7. Clear the Cart \n8. Save the Cart \n9. Provide Item Feedback \n10. Display Seller Rating \
    #               \n11. Display Buyer Purchase History \n12. Purchase the Items\n")
    #         action_number = int(input("Action Number: "))
    #         print()
    #         if action_number == 1:
    #             buyer.create_account()
    #         elif action_number == 2:
    #             buyer.logout()
    #         elif action_number == 3:
    #             buyer.search()
    #         elif action_number == 4:
    #             buyer.cart_add()
    #         elif action_number == 5:
    #             buyer.cart_remove()
    #         elif action_number == 6:
    #             buyer.cart_display()
    #         elif action_number == 7:
    #             buyer.cart_clear()
    #         elif action_number == 8:
    #             buyer.cart_save()
    #         elif action_number == 9:
    #             buyer.provide_feedback()
    #         elif action_number == 10:
    #             buyer.seller_rating()
    #         elif action_number == 11:
    #             buyer.history()
    #         elif action_number == 12:
    #             buyer.make_purchase()
