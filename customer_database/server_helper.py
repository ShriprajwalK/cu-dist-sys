import json
from customer_database.dao import Dao

def get_db_credentials():
    with open('./customer_database/credentials.json') as credentials:
        return json.load(credentials)

def jaccard_similarity(x, y):
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality / float(union_cardinality)

class ServerHelper:
    def __init__(self):
        self.dao = Dao(get_db_credentials())
        self.dao.database_init("./customer_database/init.sql")

    def choose_and_execute_action(self, action, data):
        response = {"action": action}

        response_body = {}

        action_methods = {
            "create_buyer": self.create_buyer,
            "get_buyer_id": self.get_buyer_id,
            # "search": self.search,
            # "get_rating": self.cart_add
        }

        # Get the method based on the action
        method = action_methods[action]

        if method:
            response_body = method(data)
        else:
            response_body = {"error": f"Unknown action: {action}"}

        response["body"] = response_body

        return response

    def get_buyer_id(self, data):
        username = data["body"]["username"]
        password = data["body"]["password"]
        response_body = {}
        try:
            buyer_id = self.dao.get_buyer_id(username, password)

            if buyer_id != None:
                response_body = {"buyer_id": buyer_id}
            else:
                response_body = {"buyer_id": None, "error": "Username/Password does not exist"}
        except Exception as e:
            response_body = {"buyer_id": None, "error": str(e)}

        return response_body

    def create_buyer(self, data):
        username = data["body"]["username"]
        password = data["body"]["password"]
        response_body = {}

        try:
            self.dao.create_buyer(username, password)
            response_body = {"is_created": True}
        except Exception as e:
            response_body = {"is_created": False, "error": str(e)}
        return response_body

    # def search(self, data):
    #     item_keywords = data["body"]["keywords"]
    #     item_category = data["body"]["item_category"]
    #     comparing_text = item_keywords.join(item_category)
    #     response_body = {"items": [], "message": "Search successful. Results:"}
    #     similarity_scores = []
    #     try:
    #         item_list = self.product_db.get_all_items()
    #         for item in item_list:
    #             score = jaccard_similarity(comparing_text, item[5])
    #             similarity_scores.append((score, item))

    #         similarity_scores.sort(key=lambda k: k[0], reverse=True)
    #         items_list = [i[1] for i in similarity_scores]

    #         num_of_items = 5

    #         current_item_number = 1
    #         for ranked_item in item_list:
    #             item = {"item_id": ranked_item[0], "quantity": ranked_item[2], "price": ranked_item[3],
    #                     "rating": ranked_item[4]}
    #             response_body["items"].append(item)
    #             current_item_number += 1
    #             if current_item_number == num_of_items:
    #                 break

    #         return response_body
    #     except Exception as e:
    #         return response_body

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
