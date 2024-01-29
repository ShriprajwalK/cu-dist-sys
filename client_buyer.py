import socket
import json
from prettytable import PrettyTable

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

    def check_state(self):
        if(self.id==None):
            return False
        return True

    def set_state(self, username, password, buyer_id):
        self.username = username
        self.password = password
        self.id = buyer_id

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
        request = {"action": "create_account", "type": "buyer", 'body': { "username": username, "password": password }}
        response = self.send_request(request)

        if(response["body"]["is_created"]==True):
            print("Account Created Successfully")
        else:
            print("Account Not Created : ",response["body"]["error"])

    def login(self):
        username = input("Username: ")
        password = input("Password: ")
        request = {"action": "login", "type": "buyer", 'body': { "username": username, "password": password }}
        response = self.send_request(request)

        if(response["body"]["login"]==True):
            self.set_state(username, password, response["body"]["buyer_id"])
            print("Logged In Successfully")
        else:
            print("Login Unsuccessful : ",response["body"]["error"])
        
        return response

    def logout(self):
        request = {'actions': 'logout', 'type': 'buyer', 'body': {}}
        self.reset_state()
        print("Logged Out Successfully")
        # return self.send_request(request)

    def search(self):
        item_category = input("Item Category: ")
        keywords = input("Give atleast 5 comma separated keywords: ")
        request = {"action": "search", "type": "buyer", 'body': { "item_category": item_category, 'keywords': keywords }}
        response = self.send_request(request)

        response_body = response["body"]
        table = PrettyTable(["Id","Wuantity","Price","Rating"])
        for item in response_body["items"]:
            item_id = item["item_id"]
            quantity = item["quantity"]
            price = item["price"]
            rating = item["rating"]
            table.add_row([item_id,quantity,price,rating])

        print(table)
            

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
    while(True):
        if(buyer.check_state()==False):
            print("1. Create Account \n2. Login \n")
            action_number = int(input("Action Number: "))
            if(action_number==1):
                buyer.create_account()
            elif(action_number==2):
                buyer.login()
            else:
                print("Give Appropriate Action Number")
                continue
        else:
            print("1. Create Account \n2. Logout \n")
            action_number = int(input("Action Number: "))
            if(action_number==1):
                buyer.create_account()
            elif(action_number==2):
                buyer.logout()


