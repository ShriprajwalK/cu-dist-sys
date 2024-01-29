
class BuyerServerHelper:

    def __init__(self,customer_db, product_db):
        self.customer_db = customer_db
        self.product_db = product_db

    def choose_and_execute_action(self, action, data):
        response = {"action": action, "type": "buyer"}

        if(action=="create_account"):
            response_body = self.create_account(data)
        elif(action=="login"):
            response_body = self.login(data)

        response["body"] = response_body

        return response

    def login(self,data):
            username = data["body"]["username"]
            password = data["body"]["password"]
            response_body = {}
            try:
                buyer_id = self.customer_db.check_buyer_credentials(username,password)

                if(buyer_id!=None):
                    response_body = {"login":True,"buyer_id" : buyer_id}
                else:
                    response_body = {"login":False, "error":"Username/Password does not exist"}
            except Exception as e:
                response_body = {"login":False, "error":str(e)}

            return response_body

    def create_account(self, data):
            username = data["body"]["username"]
            password = data["body"]["password"]
            response_body = {}

            try:
                self.customer_db.create_buyer(username,password)
                response_body= {"is_created":True}
            except Exception as e:
                response_body = {"is_created":False, "error":str(e)}
            return response_body