from customer_database_connect import *
from product_database_connect import *

import time
import uuid
import threading

from zeep import Client
# wsdl_url = 'http://127.0.0.1:8000/?wsdl'
# client = Client(wsdl_url)



def jaccard_similarity(x, y):
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality / float(union_cardinality)


class BuyerServerHelper:

    def __init__(self):
        self.customer_db = CustomerDatabaseConnection("localhost", 8994)
        self.product_db = ProductDatabaseConnection("localhost", 9005)

    def login(self, data):
        username = data["body"]["username"]
        password = data["body"]["password"]
        response_body = {}
        try:
            buyer_id = self.customer_db.get_buyer_by_id(username, password)
            if buyer_id != None:
                response_body = {"login": True, "buyer_id": buyer_id, 'message': 'Login successful',
                                 'session_id': data['body']['session_id']}
            else:
                response_body = {"login": False, "error": "Username/Password does not exist"}
        except Exception as e:
            print(e)
            response_body = {"login": False, "error": str(e)}

        return response_body

    def create_account(self, data):
        username = data["body"]["username"]
        password = data["body"]["password"]
        response_body = {}

        try:
            is_created = self.customer_db.create_buyer(username, password)
            if is_created == False:
                response_body = {"is_created": False, "message": 'Account not created'}
            else:
                response_body = {"is_created": True, "message": 'Account created Successfully'}

        except Exception as e:
            print(e)
            response_body = {"is_created": False, "error": str(e)}
        return response_body

    def search(self, data):
        item_keywords = data["body"]["keywords"]
        requested_category = data["body"]["item_category"]

        response_body = {"items": [], "message": "Search successful. Results:"}
        similarity_scores = []
        try:
            item_list = self.product_db.get_all_items()
            for item in item_list:
                item_category = item[7]
                if (item_category == requested_category):
                    score = jaccard_similarity(item_keywords, item[5])
                    similarity_scores.append((score, item))

            similarity_scores.sort(key=lambda k: k[0], reverse=True)
            items_list = [i[1] for i in similarity_scores]

            num_of_items = 5

            current_item_number = 1
            for ranked_item in items_list:
                item = {"item_name": ranked_item[6], "item_id": ranked_item[0], "quantity": ranked_item[2],
                        "price": ranked_item[3],
                        "rating": ranked_item[4]}
                response_body["items"].append(item)
                current_item_number += 1
                if current_item_number == num_of_items:
                    break

            return response_body
        except Exception as e:
            print(e)
            response_body = {"items": [], "message": "Search unsuccessful because:" + str(e)}
            return response_body

    def get_all_items(self, data):
        response_body = {"items": []}
        try:
            item_list = self.product_db.get_all_items()
            for item in item_list:
                item_map = {"item_id": item[0], "quantity": item[2], "price": item[3],
                            "rating": item[4]}
                response_body["items"].append(item_map)
            return response_body
        except Exception as e:
            print(e)
            response_body = {"items": None, }
            return response_body

    def cart_add(self, data):
        item_id = data["body"]["item_id"]
        buyer_id = data["body"]["buyer_id"]
        requested_quantity = data["body"]["quantity"]
        response_body = {}

        try:
            item = self.product_db.get_item_by_id(item_id)
            available_quantity = item['quantity']
            item_name = item['name']
            print("available_quantity:", available_quantity)
            if requested_quantity >= available_quantity:
                response_body = {"add": False, "message": "Requested Quantity Not Present in the Database"}
            else:
                print("===Get cart item")
                cart_item = self.customer_db.get_cart_item(item_id, buyer_id)
                print("cart_item", cart_item, type(cart_item))
                print("===Get item price")
                price = self.product_db.get_item_price(item_id)
                is_added = False
                if cart_item == None:
                    print("===add to cart")
                    is_added = self.customer_db.add_to_cart(item_name, item_id, buyer_id, requested_quantity, price)
                else:
                    print("===update cart item quantity")
                    original_quantity = cart_item['quantity']
                    is_added = self.customer_db.update_cart_item_quantity(item_id, buyer_id,
                                                                          original_quantity + requested_quantity)

                if is_added:
                    response_body = {"add": True, "message": "Item added to cart"}
                else:
                    response_body = {"add": False, "message": "Item not added to cart"}
            return response_body
        except Exception as e:
            print(e)
            return {"add": False, "message": "Item Not Present in the Database"}

    def get_purchase_history(self, data):
        buyer_id = data["body"]["buyer_id"]
        response_body = {"items": []}
        try:
            print("buyer_id", buyer_id)
            purchased_items = self.customer_db.get_purchase_history(buyer_id)

            for purchased_item in purchased_items:
                item_info = {}
                item_info["item_name"] = purchased_item[4]
                item_info["item_id"] = purchased_item[2]
                item_info["quantity"] = purchased_item[3]
                response_body["items"].append(item_info)
            return response_body
        except Exception as e:
            print(e)
            response_body = {"items": None}
            return response_body

    def item_rating(self, data):
        item_rating_map = data["body"]["rating"]
        int_item_rating_map = {}
        for item_id in item_rating_map:
            int_item_rating_map[int(item_id)] = item_rating_map[item_id]
        try:
            items = self.product_db.get_all_items()
            for item in items:
                item_id = item[0]
                item_rating = item[4]
                if (item_id in int_item_rating_map.keys()):
                    item_rating += int_item_rating_map[item_id]
                    self.product_db.update_item_rating(item_id, item_rating)
                    seller_id = self.product_db.get_item_seller_id(item_id)
                    print("seller_id", seller_id)
                    self.product_db.update_seller_rating(seller_id, int_item_rating_map[item_id])
            return {"success": True}
        except Exception as e:
            print(e)
            return {"success": False}

    def cart_clear(self, data):
        buyer_id = data["body"]["buyer_id"]

        try:
            is_cleared = self.customer_db.delete_cart_by_buyer_id(buyer_id)

            if (is_cleared):
                return {"cleared": True}
            else:
                return {"cleared": False}
        except Exception as e:
            print(e)
            return {"cleared": False}

    def cart_remove(self, data):
        item_id = data["body"]["item_id"]
        removing_quantity = data["body"]["quantity"]
        buyer_id = data["body"]["buyer_id"]

        try:
            cart_item = self.customer_db.get_cart_item(item_id, buyer_id)

            if (cart_item == None):
                return {"removed": False}
            original_quantity = cart_item[3]
            if (original_quantity <= removing_quantity):
                success = self.customer_db.remove_cart_item(item_id, buyer_id)
                return {"removed": success}
            else:
                self.customer_db.update_cart_item_quantity(item_id, buyer_id, original_quantity - removing_quantity)
                return {"removed": True}
        except Exception as e:
            print(e)
            return {"removed": False}

    def cart_display(self, data):
        buyer_id = data["body"]["buyer_id"]
        response_body = {"items": []}
        try:

            cart_items = self.customer_db.get_buyer_cart_items(buyer_id)
            print("DIAPLAY CART", cart_items)
            for item in cart_items:
                item_map = {}
                item_map["item_name"] = item['name']
                item_map["item_id"] = item['id']
                item_map["quantity"] = item['quantity']
                # item_map["price"] = item['price']
                response_body["items"].append(item_map)
            print(response_body)
            return response_body

        except Exception as e:
            print(e)
            return {"items": None}

    def seller_rating(self, data):
        seller_id = data["body"]["seller_id"]
        response_body = {"rating": None}
        try:

            rating = self.product_db.get_seller_rating(seller_id)
            response_body["rating"] = rating
            return response_body

        except Exception as e:
            print(e)
            return response_body

    def cart_save(self, data):
        buyer_id = data["body"]["buyer_id"]
        response_body = {"saved": False}
        try:
            response_body["saved"] = True
            return response_body

        except Exception as e:
            print(e)
            return response_body

    def logout(self, data,sessions):
        if 'session_id' in data['body']:
            del sessions[data['body']['session_id']]


    def purchase(self, data):
        buyer_id = data["body"]["buyer_id"]
        # response = client.service.process_transaction(buyer_id, 123123123)
        # return {'status': response}
