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
        self.cart = []

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
            print("Account Created Successfully \n")
        else:
            print("Account Not Created : ",response["body"]["error"],"\n")

    def login(self):
        username = input("Username: ")
        password = input("Password: ")
        request = {"action": "login", "type": "buyer", 'body': { "username": username, "password": password }}
        response = self.send_request(request)

        if(response["body"]["login"]==True):
            self.set_state(username, password, response["body"]["buyer_id"])
            print("Logged In Successfully \n")
        else:
            print("Login Unsuccessful : ",response["body"]["error"],"\n")
        
        return response

    def logout(self):
        request = {'actions': 'logout', 'type': 'buyer', 'body': {}}
        self.reset_state()
        print("Logged Out Successfully \n")

    def search(self):
        item_category = input("Item Category: ")
        keywords = input("Give atleast 5 comma separated keywords: ")
        request = {"action": "search", "type": "buyer", 'body': { "item_category": item_category, 'keywords': keywords }}
        response = self.send_request(request)

        response_body = response["body"]
        table = PrettyTable(["Id","Quantity","Price","Rating"])
        for item in response_body["items"]:
            item_id = item["item_id"]
            quantity = item["quantity"]
            price = item["price"]
            rating = item["rating"]
            table.add_row([item_id,quantity,price,rating])

        print(table ,"\n")
            

    def cart_add(self):
        item_id = int(input("Item Id: "))
        quantity = int(input("Quantity: "))
        request = {"action": "cart_add", "type": "buyer", 'body': { "item_id": item_id, 'quantity': quantity}}
        response = self.send_request(request)

        response_body = response["body"]

        if(response_body["add"]==True):
            self.cart.append(response_body["item_details"])
            print("Item Added to the Cart" ,"\n")
        else:
            print("Could Not add to the because:", response_body["Reason"] ,"\n")

    def cart_remove(self, item, num):
        # request = {"action": "cart_remove", "type": "buyer", 'body': { "item": item, 'quantity': num}}
        # return self.send_request(request)
        item_id = int(input("Item Id: "))
        quantity = int(input("Quantity: "))
        item_removed = False
        for item_num in range(len(self.cart)):
            if(self.cart[item_num][0]==item_id):
                self.cart[item_num][1]-= quantity
                if (self.cart[item_num][1]<=0):
                    self.cart.pop(item_num) 
                item_removed = True
        
        if(item_removed==True):
            print("Item Successfully Removed")
        else:
            print("Item Not Found in the Cart")


    def cart_display(self):
        # request = {"action": "cart_display", "type": "buyer", 'body': {}}
        # return self.send_request(request)
        table = PrettyTable(["Id","Quantity","Price"])
        for item in self.cart:
            table.add_row([item[0],item[1],item[2]])

        print(table ,"\n")

    def cart_clear(self):
        # request = {"action": "cart_clear", "type": "buyer", 'body': {}}
        # return self.send_request(request)
        self.cart = []
        print("Cart Cleared")


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
            print()
            if(action_number==1):
                buyer.create_account()
            elif(action_number==2):
                buyer.login()
            else:
                print("Give Appropriate Action Number")
                continue
        else:
            print("1. Create Account \n2. Logout \n3. Search Items \n4. Add Items to Cart \n5. Remote Item From Cart \
                  \n6. Display Cart \n7. Clear the Cart \n8. Save the Cart \n9. Provide Item Feedback \n10. Display Seller Rating \
                  \n11. Display Buyer Purchase History \n12. Purchase the Items\n")
            action_number = int(input("Action Number: "))
            print()
            if(action_number==1):
                buyer.create_account()
            elif(action_number==2):
                buyer.logout()
            elif(action_number==3):
                buyer.search()
            elif(action_number==4):
                buyer.cart_add()
            elif(action_number==5):
                buyer.cart_remove()
            elif(action_number==6):
                buyer.cart_display()
            elif(action_number==7):
                buyer.cart_clear()
            elif(action_number==8):
                buyer.cart_save()
            elif(action_number==9):
                buyer.provide_feedback()
            elif(action_number==10):
                buyer.seller_rating()
            elif(action_number==11):
                buyer.history()
            elif(action_number==12):
                buyer.make_purchase()
            



