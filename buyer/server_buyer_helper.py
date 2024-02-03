from buyer.customer_database_connect import *
from buyer.product_database_connect import *

def jaccard_similarity(x, y):
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality / float(union_cardinality)


class BuyerServerHelper:

    def __init__(self):
        self.customer_db = CustomerDatabaseConnection("localhost",9000)
        self.product_db = ProductDatabaseConnection("localhost",9001)
        # self.product_db = product_db

    def choose_and_execute_action(self, action, data):
        response = {"action": action, "type": "buyer"}

        response_body = {}

        action_methods = {
            "create_account": self.create_account,
            "login": self.login,
            "search": self.search,
            "get_rating": self.cart_add
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
            buyer_id = self.customer_db.get_buyer_by_id(username, password)
            if buyer_id != None:
                response_body = {"login": True, "buyer_id": buyer_id, 'message': 'Login successful'}
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
            is_created = self.customer_db.create_buyer(username, password)
            if is_created==False:
                response_body = {"is_created": False, "message": 'Account not created'}
            else:
                response_body = {"is_created": True, "message": 'Account created Successfully'}
            
        except Exception as e:
            response_body = {"is_created": False, "error": str(e)}
        return response_body

    def search(self, data):
        item_keywords = data["body"]["keywords"]
        item_category = data["body"]["item_category"]
        comparing_text = item_keywords.join(item_category)
        response_body = {"items": [], "message": "Search successful. Results:"}
        similarity_scores = []
        try:
            item_list = self.product_db.get_all_items()
            for item in item_list:
                score = jaccard_similarity(comparing_text, item[5])
                similarity_scores.append((score, item))

            similarity_scores.sort(key=lambda k: k[0], reverse=True)
            items_list = [i[1] for i in similarity_scores]

            num_of_items = 5

            current_item_number = 1
            for ranked_item in items_list:
                item = {"item_id": ranked_item[0], "quantity": ranked_item[2], "price": ranked_item[3],
                        "rating": ranked_item[4]}
                response_body["items"].append(item)
                current_item_number += 1
                if current_item_number == num_of_items:
                    break

            return response_body
        except Exception as e:
            response_body = {"items": [], "message": "Search unsuccessful because:"+str(e)}
            return response_body

    def cart_add(self, data):
        item_id = data["body"]["item_id"]
        requested_quantity = data["body"]["quantity"]
        response_body = {}

        try:
            item = self.product_db.get_item_by_id(item_id)
            available_quantity = item[2]
            price = item[3]
            if requested_quantity >= available_quantity:
                return {"add": False, "message": "Requested Quantity Not Present in the Database"}

            item_details = [item_id, requested_quantity, price]

            response_body = {"add": True, "item_details": item_details, "message": "Item added to cart"}
            return response_body
        except Exception as e:
            print(e)
            return {"add": False, "message": "Item Not Present in the Database"}
