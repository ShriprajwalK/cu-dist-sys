from product_database_connect import ProductDatabaseConnection
import time
import uuid
import threading


class SellerServerHelper:
    def __init__(self):
        self.product_db = ProductDatabaseConnection("localhost", 9005)
        self.sessions = {}

    def login(self, data):
        username = data["body"]["username"]
        password = data["body"]["password"]
        response_body = {}
        try:
            seller_id = self.product_db.get_seller_by_id(username, password)

            if seller_id is not None:
                response_body = {"login": True, "message": 'Logged in successfully', "seller_id": seller_id,
                                 'session_id': data["body"]["session_id"]}
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
        added_item = self.product_db.sell_item(seller, name, category, keywords, condition, price, quantity)
        response_body = {"added_item": added_item}
        return response_body

    def update_price(self, data):
        item_id = data['body']['item_id']
        price = data['body']['price']
        updated_item = self.product_db.update_price(item_id, price)
        response_body = {"updated_item": updated_item}
        return response_body

    def get_items_for_seller(self, data):
        seller_id = data['body']['seller_id']
        items = self.product_db.get_items_for_seller(seller_id)
        response_body = {"items": items}
        return response_body

    def remove_item(self, data):
        item_id = data['body']['item_id']
        quantity = data['body']['quantity']
        removed = self.product_db.remove_item(item_id, quantity)
        response_body = {"removed": removed}
        return response_body

    def logout(self, data, sessions):
        if 'session_id' in data['body']:
            del sessions[data['body']['session_id']]

