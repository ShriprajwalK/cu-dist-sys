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
        self.dao.database_init("./product_database/init.sql")

    def choose_and_execute_action(self, action, data):
        response = {"action": action}

        response_body = {}

        action_methods = {
            "create_seller": self.create_seller,
            "get_seller_id": self.get_seller_id,
            "get_all_items":self.get_all_items
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


    # def cart_add(self, data):
    #     item_id = data["body"]["item_id"]
    #     requested_quantity = data["body"]["quantity"]
    #     response_body = {}

    #     try:
    #         item = self.product_db.get_item_by_id(item_id)
    #         available_quantity = item[2]
    #         price = item[3]
    #         if requested_quantity >= available_quantity:
    #             return {"add": False, "message": "Requested Quantity Not Present in the Database"}

    #         item_details = [item_id, requested_quantity, price]

    #         response_body = {"add": True, "item_details": item_details, "message": "Item added to cart"}
    #         return response_body
    #     except Exception as e:
    #         print(e)
    #         return {"add": False, "message": "Item Not Present in the Database"}
