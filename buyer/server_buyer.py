import json
from buyer.server_buyer_helper import *
import requests
from flask import Flask, jsonify, request
from buyer.sessions_manager import *
from logging.config import dictConfig
import sys
app = Flask(__name__)


class BuyerServer:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port

        self.server_buyer_helper = BuyerServerHelper()
        self.sessions_manager = SessionsManager()
        self.setup_routes()
        self.session_cleaner()

    def run(self):
        app.run(host=self.server_host, port=self.server_port)

    def session_cleaner(self):
        cleaner_thread = threading.Thread(target=self.sessions_manager.session_cleaner, daemon=True)
        cleaner_thread.start()
    
    def manage_sessions(self, data):
        session = self.sessions_manager.manage_session(data)
        if not session['exists']:
            data['body']['session_id'] = session['session_id']
        return data
    
    def setup_routes(self):
        
        @app.route('/login', methods=['GET'])
        def login():
            data = request.get_json()
            data = self.manage_sessions(data)

            response_data = self.server_buyer_helper.login(data)
            return response_data
        
        @app.route('/create_account', methods=['PUT'])
        def create_account():
            data = request.get_json()
            data = self.manage_sessions(data)

            response_data = self.server_buyer_helper.create_account(data)
            return response_data
        
        @app.route('/search', methods=['GET'])
        def search():
            data = request.get_json()
            data = self.manage_sessions(data)

            response_data = self.server_buyer_helper.search(data)
            return response_data
        
        @app.route('/cart_add', methods=['PUT'])
        def cart_add():
            data = request.get_json()
            data = self.manage_sessions(data)

            response_data = self.server_buyer_helper.cart_add(data)
            return response_data
        
        @app.route('/cart_remove', methods=['DELETE'])
        def cart_remove():
            data = request.get_json()
            data = self.manage_sessions(data)

            response_data = self.server_buyer_helper.cart_remove(data)
            return response_data
        
        @app.route('/cart_display', methods=['GET'])
        def cart_display():
            data = request.get_json()
            data = self.manage_sessions(data)
            response_data = self.server_buyer_helper.cart_display(data)
            return response_data
        
        @app.route('/cart_save', methods=['PUT'])
        def cart_save():
            data = request.get_json()
            data = self.manage_sessions(data)

            response_data = self.server_buyer_helper.cart_save(data)
            return response_data
        
        @app.route('/get_purchase_history', methods=['GET'])
        def get_purchase_history():
            data = request.get_json()
            data = self.manage_sessions(data)

            response_data = self.server_buyer_helper.get_purchase_history(data)
            return response_data
        
        @app.route('/item_rating', methods=['PUT'])
        def item_rating():
            data = request.get_json()
            data = self.manage_sessions(data)

            response_data = self.server_buyer_helper.item_rating(data)
            return response_data
        
        @app.route('/seller_rating', methods=['GET'])
        def seller_rating():
            data = request.get_json()
            data = self.manage_sessions(data)

            response_data = self.server_buyer_helper.seller_rating(data)
            return response_data
        
        @app.route('/cart_clear', methods=['DELETE'])
        def cart_clear():
            data = request.get_json()
            data = self.manage_sessions(data)

            response_data = self.server_buyer_helper.cart_clear(data)
            return response_data
        
        @app.route('/purchase', methods=['POST'])
        def purchase():
            data = request.get_json()
            data = self.manage_sessions(data)

            response_data = self.server_buyer_helper.purchase(data)
            return response_data
        

if __name__ == "__main__":
    server_host = "127.0.0.1"
    server_port = 1234

    buyer_server = BuyerServer(server_host, server_port)
    buyer_server.run()
