# import json
# from dao import Dao
#
# def get_db_credentials():
#     with open('./customer_database/credentials.json') as credentials:
#         return json.load(credentials)
#
# def jaccard_similarity(x, y):
#     intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
#     union_cardinality = len(set.union(*[set(x), set(y)]))
#     return intersection_cardinality / float(union_cardinality)
#
# class ServerHelper:
#     def __init__(self):
#         self.dao = Dao(get_db_credentials())
#         self.dao.database_init("./customer_database/init.sql")
#
#     def choose_and_execute_action(self, action, data):
#         response = {"action": action}
#
#         response_body = {}
#
#         action_methods = {
#             "create_buyer": self.create_buyer,
#             "get_buyer_id": self.get_buyer_id,
#             "get_buyer_purchase":self.get_buyer_purchase,
#             "create_cart":self.create_cart,
#             "delete_cart_by_buyer_id":self.delete_cart_by_buyer_id,
#             "get_cart_item":self.get_cart_item,
#             "update_cart_item_quantity":self.update_cart_item_quantity,
#             "remove_cart_item":self.remove_cart_item,
#             "get_buyer_cart_items":self.get_buyer_cart_items
#         }
#
#         # Get the method based on the action
#         method = action_methods[action]
#
#         if method:
#             response_body = method(data)
#         else:
#             response_body = {"error": f"Unknown action: {action}"}
#
#         response["body"] = response_body
#
#         return response
#
#     def get_buyer_id(self, data):
#         username = data["body"]["username"]
#         password = data["body"]["password"]
#         response_body = {}
#         try:
#             buyer_id = self.dao.get_buyer_id(username, password)
#
#             if buyer_id != None:
#                 response_body = {"buyer_id": buyer_id}
#             else:
#                 response_body = {"buyer_id": None, "error": "Username/Password does not exist"}
#         except Exception as e:
#             print(e)
#             response_body = {"buyer_id": None, "error": str(e)}
#
#         return response_body
#
#     def create_buyer(self, data):
#         username = data["body"]["username"]
#         password = data["body"]["password"]
#         response_body = {}
#
#         try:
#             self.dao.create_buyer(username, password)
#             response_body = {"is_created": True}
#         except Exception as e:
#             print(e)
#             response_body = {"is_created": False, "error": str(e)}
#         return response_body
#
#     def get_buyer_purchase(self, data):
#         buyer_id = data["body"]["buyer_id"]
#         response_body = {}
#
#         try:
#             items = self.dao.get_buyer_purchase(buyer_id)
#             response_body = {"items": items}
#         except Exception as e:
#             print(e)
#             response_body = {"items": None, "error": str(e)}
#         return response_body
#
#     def create_cart(self, data):
#         item_name = data["body"]["item_name"]
#         item_id = data["body"]["item_id"]
#         buyer_id = data["body"]["buyer_id"]
#         quantity = data["body"]["quantity"]
#         price = data["body"]["price"]
#         try:
#             self.dao.create_cart(item_name, item_id,buyer_id, quantity, price)
#             response_body = {"is_created": True}
#         except Exception as e:
#             print(e)
#             response_body = {"is_created": False, "error": str(e)}
#         return response_body
#
#
#     def delete_cart_by_buyer_id(self, data):
#         buyer_id = data["body"]["buyer_id"]
#         try:
#             self.dao.delete_cart_by_buyer_id(buyer_id)
#             response_body = {"deleted": True}
#         except Exception as e:
#             print(e)
#             response_body = {"deleted": False, "error": str(e)}
#         return response_body
#
#     def get_cart_item(self, data):
#         item_id = data["body"]["item_id"]
#         buyer_id = data["body"]["buyer_id"]
#
#         try:
#             item = self.dao.get_cart_item(item_id, buyer_id)
#             response_body = {"item": item}
#         except Exception as e:
#             print(e)
#             response_body = {"item": None, "error": str(e)}
#         return response_body
#
#     def update_cart_item_quantity(self, data):
#         item_id = data["body"]["item_id"]
#         buyer_id = data["body"]["buyer_id"]
#         quantity = data["body"]["quantity"]
#
#         try:
#             self.dao.update_cart_item_quantity(item_id, buyer_id, quantity)
#             response_body = {"updated": True}
#         except Exception as e:
#             print(e)
#             response_body = {"updated": False, "error": str(e)}
#         return response_body
#
#
#     def remove_cart_item(self, data):
#         item_id = data["body"]["item_id"]
#         buyer_id = data["body"]["buyer_id"]
#
#         try:
#             self.dao.remove_cart_item(item_id, buyer_id)
#             response_body = {"removed": True}
#         except Exception as e:
#             print(e)
#             response_body = {"removed": False, "error": str(e)}
#         return response_body
#
#     def get_buyer_cart_items(self, data):
#         buyer_id = data["body"]["buyer_id"]
#         print("buyer_id",buyer_id)
#         try:
#             items = self.dao.get_buyer_cart_items(buyer_id)
#             response_body = {"items": items}
#             print(response_body)
#         except Exception as e:
#             print(e)
#             response_body = {"items": None, "error": str(e)}
#         return response_body
#
#
#
#
