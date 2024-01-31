class SellerServerHelper:

    def __init__(self, customer_db, product_db):
        self.customer_db = customer_db
        self.product_db = product_db

    def choose_and_execute_action(self, action, data):
        response = {"action": action, "type": "seller"}

        action_methods = {
            "create_account": self.create_account,
            "login": self.login,
            "search": self.search,
        }

        # Get the method based on the action
        method = action_methods[action]

        if method:
            response_body = method(data)
        else:
            response_body = {"error": f"Unknown action: {action}"}

        response["body"] = response_body

        return response

    def login(self, data):
        username = data["body"]["username"]
        password = data["body"]["password"]
        response_body = {}
        try:
            seller_id = self.product_db.check_seller_credentials(username, password)

            if seller_id is not None:
                response_body = {"login": True, "message": 'Logged in successfully', "buyer_id": seller_id}
            else:
                response_body = {"login": False, "error": "Username/Password does not exist"}
        except Exception as e:
            response_body = {"login": False, "error": str(e)}

        return response_body

    def create_account(self, data):
        username = data["body"]["username"]
        password = data["body"]["password"]
        response_body = {}

        try:
            self.product_db.create_seller(username, password)
            response_body = {"is_created": True, "message": "Account created successfully"}
        except Exception as e:
            response_body = {"is_created": False, "error": str(e)}
        return response_body

    def logout(self, data):
        pass

