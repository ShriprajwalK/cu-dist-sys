from .product_database_connect import ProductDatabaseConnection


# from ..helper.helper import get_credentials


def get_credentials(data):
    if 'body' in data and 'username' in data['body'] and 'password' in data['body']:
        return {'username': data['body']['username'], 'password': data['body']['password']}
    else:
        return False


class SellerServerHelper:
    def __init__(self):
        self.product_db = ProductDatabaseConnection("localhost", 9001)
        self.user_cache = {}

    def validate_request(self, cred):
        if cred['username'] in self.user_cache:
            if cred['password'] == self.user_cache[cred['username']]:
                return {'requestor': self.user_cache[cred['username']['password']]}
            else:
                return {'error': 'Permission denied'}
        #else:
            # insert timeout check here
            # seller = self.product_db.get_seller_by_id(cred['username'], cred['password'])
            # if seller is not None:
            #    return {'requester': seller}
            # else:
            #    return {'error': 'Permission denied'}

    def choose_and_execute_action(self, action, data):
        response = {"action": action, "type": "seller"}

        action_methods = {
            "create_account": self.create_account,
            "login": self.login,
            "get_rating": self.get_rating,
            'update_price': self.update_price,
            'remove_item': self.remove_item,
            'sell': self.sell,
            'get_items_for_seller': self.get_items_for_seller,
        }

        method = action_methods[action]
        cred = get_credentials(data)
        if cred:
            valid_info = self.validate_request(cred)
            if valid_info:
                if 'error' in valid_info:
                    return valid_info
                else:
                    data['body']['requestor'] = valid_info['requestor']

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
            seller_id = self.product_db.get_seller_by_id(username, password)

            if seller_id is not None:
                response_body = {"login": True, "message": 'Logged in successfully', "seller_id": seller_id}
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

    def get_rating(self, data):
        seller = data['body']['seller_id']
        rating = self.product_db.get_seller_rating_by_id(seller)
        response_body = {"rating": rating}
        return response_body

    def sell(self, data):
        seller = data["body"]["seller_id"]
        name = data['body']['name']
        category = data['body']['category']
        keywords = data['body']['keywords']
        condition = data['body']['condition']
        price = data['body']['price']
        quantity = data['body']['quantity']
        self.product_db.sell_item(seller, name, category, keywords, condition, price, quantity)

    def update_price(self, data):
        item_id = data['body']['item_id']
        price = data['body']['price']
        response = self.product_db.update_price(item_id, price)
        return response

    def get_items_for_seller(self, data):
        seller_id = data['body']['seller_id']
        items = self.product_db.get_items_for_seller(seller_id)
        return items

    def remove_item(self, data):
        item_id = data['body']['item_id']
        quantity = data['body']['quantity']
        response = self.product_db.remove_item(item_id, quantity)
        return response

    def logout(self, data):
        pass
