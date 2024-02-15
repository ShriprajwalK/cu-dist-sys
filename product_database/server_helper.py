import json
from product_database.dao import Dao

def get_db_credentials():
    with open('./product_database/credentials.json') as credentials:
        return json.load(credentials)

def jaccard_similarity(x, y):
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality / float(union_cardinality)

class ServerHelper:
    def __init__(self):
        self.dao = Dao(get_db_credentials())
        # self.dao.database_init("./product_database/init.sql")

    def choose_and_execute_action(self, action, data):
        response = {"action": action}

        response_body = {}

        action_methods = {
            "create_seller": self.create_seller,
            "get_seller_id": self.get_seller_id,
            "get_all_items":self.get_all_items,
            "update_item_rating":self.update_item_rating,
            "get_item_seller_id":self.get_item_seller_id,
            "update_seller_rating":self.update_seller_rating,
            "get_item_by_id":self.get_item_by_id,
            "get_item_price":self.get_item_price,
            "get_seller_rating":self.get_seller_rating,
            'sell_item': self.sell_item,
            'update_price': self.update_price,
            'get_items_for_seller': self.get_items_for_seller,
            'remove_item': self.remove_item
        }

        # Get the method based on the action
        method = action_methods[action]

        if method:
            response_body = method(data)
        else:
            response_body = {"error": f"Unknown action: {action}"}

        response["body"] = response_body

        return response

    def get_seller_id(self, data):
        username = data["body"]["username"]
        password = data["body"]["password"]
        response_body = {}
        print()
        try:
            seller_id = self.dao.get_seller_id(username, password)

            if seller_id != None:
                response_body = {"seller_id": seller_id}
            else:
                response_body = {"seller_id": None, "error": "Username/Password does not exist"}
        except Exception as e:
            response_body = {"seller_id": None, "error": str(e)}

        return response_body

    def create_seller(self, data):
        username = data["body"]["username"]
        password = data["body"]["password"]
        response_body = {}

        try:
            self.dao.create_seller(username, password)
            response_body = {"is_created": True}
        except Exception as e:
            response_body = {"is_created": False, "error": str(e)}
        return response_body
    
    def get_all_items(self,data):
        try:
            items = self.dao.get_all_items()
            response_body = {"items": items}
        except Exception as e:
            response_body = {"items": None}
        return response_body
    
    def get_item_by_id(self, data):
        item_id = data["body"]["item_id"]
        try:
            item = self.dao.get_item_by_id(item_id)
            response_body = {"item": item}
        except Exception as e:
            response_body = {"item": None}
        return response_body
    
    def update_item_rating(self, data):
        print("data",data)
        item_id = data["body"]["item_id"]
        item_rating = data["body"]["item_rating"]

        try:
            self.dao.update_item_rating(item_id, item_rating)
            response_body = {"success": True}
        except Exception as e:
            response_body = {"success": False, "error": str(e)}
        return response_body
    
    def get_item_seller_id(self, data):
        item_id = data["body"]["item_id"]
        try:
            seller_id = self.dao.get_item_seller_id(item_id)
            response_body = {"seller_id": seller_id}
        except Exception as e:
            response_body = {"seller_id": None}
        return response_body
    
    def update_seller_rating(self, data):
        seller_id = data["body"]["seller_id"]
        item_rating = data["body"]["item_rating"]

        try:
            self.dao.update_seller_rating(seller_id, item_rating)
            response_body = {"success": True}
        except Exception as e:
            response_body = {"success": False, "error": str(e)}
        return response_body
    
    def get_item_price(self, data):
        item_id = data["body"]["item_id"]
        try:
            price = self.dao.get_item_price(item_id)
            response_body = {"price": price}
        except Exception as e:
            response_body = {"price": None}
        return response_body
    

    def get_seller_rating(self, data):
        seller_id = data["body"]["seller_id"]
        try:
            rating = self.dao.get_seller_rating(seller_id)
            response_body = {"rating": rating}
        except Exception as e:
            print(e)
            response_body = {"rating": None, "error": str(e)}
        return response_body

    def sell_item(self, data):
        seller_id = data["body"]["seller_id"]
        name = data['body']['name']
        category = data['body']['category']
        keywords = data['body']['keywords']
        condition = data['body']['condition']
        price = data['body']['price']
        quantity = data['body']['quantity']
        try:
            print("SELLING ITEM")
            self.dao.sell_item(seller_id, name, category, keywords, condition, price, quantity)
            response_body = {"response": "Successfully added item to sell"}
        except Exception as e:
            print(e)
            response_body = {"error": str(e)}
        return response_body


    def get_items_for_seller(self, data):
        seller_id = data["body"]["seller_id"]
        try:
            items = self.dao.get_items_for_seller(seller_id)
            print("ITEMS")
            response_body = {"items": items}
        except Exception as e:
            print(e)
            response_body = {"error": str(e)}
        return response_body

    def remove_item(self, data):
        item_id = data["body"]["item_id"]
        quantity = data["body"]["quantity"]
        try:
            message = self.dao.remove_item(item_id, quantity)
            response_body = {"message": "Removed items succesffully"}
        except Exception as e:
            print(e)
            response_body = {"error": str(e)}
        return response_body

        pass

    def update_price(self, data):
        item_id = data["body"]["item_id"]
        price = data["body"]["price"]
        try:
            message = self.dao.update_price(item_id, price)
            response_body = {"message": "Updated price succesffully"}
        except Exception as e:
            print(e)
            response_body = {"error": str(e)}
        return response_body
        pass

