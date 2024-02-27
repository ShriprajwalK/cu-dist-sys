import socket
import psycopg2
import json
from server_seller_helper import *
import sys
from sessions_manager import *
from flask import Flask, jsonify, request

app = Flask(__name__)


class SellerServer:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port

        self.server_seller_helper = SellerServerHelper()
        self.sessions_manager = SessionsManager()
        self.setup_routes()
        self.session_cleaner()

        self.operations = 0
        self.start = time.time()
        self.max = 0

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
            self.operations += 1
            response_data = self.server_seller_helper.login(data)
            self.max = max(self.max, self.operations / (time.time() - self.start))
            print(self.max)
            return response_data

        @app.route('/create_account', methods=['PUT'])
        def create_account():
            data = request.get_json()
            data = self.manage_sessions(data)

            response_data = self.server_seller_helper.create_account(data)
            return response_data
        
        @app.route('/get_rating', methods=['GET'])
        def get_rating():
            data = request.get_json()
            data = self.manage_sessions(data)
            self.operations += 1
            response_data = self.server_seller_helper.get_rating(data)
            self.max = max(self.max, self.operations / (time.time() - self.start))
            print(self.max)
            return response_data
        
        @app.route('/sell', methods=['POST'])
        def sell():
            data = request.get_json()
            data = self.manage_sessions(data)

            response_data = self.server_seller_helper.sell(data)
            return response_data
        
        @app.route('/update_price', methods=['POST'])
        def update_price():
            data = request.get_json()
            data = self.manage_sessions(data)

            response_data = self.server_seller_helper.update_price(data)
            return response_data
        
        @app.route('/get_items_for_seller', methods=['GET'])
        def get_items_for_seller():
            data = request.get_json()
            data = self.manage_sessions(data)
            response_data = self.server_seller_helper.get_items_for_seller(data)
            return response_data
        
        @app.route('/cart_save', methods=['PUT'])
        def cart_save():
            data = request.get_json()
            data = self.manage_sessions(data)

            response_data = self.server_seller_helper.cart_save(data)
            return response_data
        
        @app.route('/remove_item', methods=['DELETE'])
        def remove_item():
            data = request.get_json()
            data = self.manage_sessions(data)

            response_data = self.server_seller_helper.remove_item(data)
            return response_data
    


if __name__ == "__main__":
    server_host = "localhost"
    server_port = 1235

    seller_server = SellerServer(server_host, server_port)
    seller_server.run()
