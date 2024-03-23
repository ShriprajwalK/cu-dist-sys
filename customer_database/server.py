import socket
import sys
import json
from concurrent import futures
import grpc
import customer_service_pb2
import customer_service_pb2_grpc
from dao import Dao
from grpc import ServerInterceptor, ServicerContext, RpcMethodHandler
# from server_helper import ServerHelper
import requests

import threading
from flask import Flask, jsonify, request

app = Flask(__name__)


def send_request(request_data, url):
    print("in send request")

    headers = {'Content-type': 'application/json'}
    url_path = "http://" + url + "/" + 'sequence'

    print('sending request to::', url_path)
    response = requests.post(url=url_path, data=json.dumps(request_data), headers=headers)
    print('done sending request')
    print(response.json())
    return response.json()


class RotatingSequencerServer:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port

        self.local_seq_number = 0
        self.global_seq_number = 0
        self.nodes = ["0.0.0.0:4444", "0.0.0.0:4445"]
        self.client_for_nodes = {}
        self.node_id = self.server_port % 4444

        self.setup_routes()

    def run(self):
        print("NODE_ID::", self.node_id)
        for i in self.nodes:
            port = int(i.split(":")[1]) + 4550
            self.client_for_nodes[i] = customer_service_pb2_grpc.CustomerServiceStub(grpc.insecure_channel("0.0.0.0:"+str(port)))
            print("Added grpc client for port::", port)
        app.run(host=self.server_host, port=self.server_port)

    def send_request_to_nodes_follower(self, path, data):
        print("sending follower requests")
        data['local_sequence_number'] = self.server_host + str(self.server_port) + str(self.local_seq_number)
        for i in self.nodes:
            print(data)
            request_data = {"path": path, 'data': data}
            response = send_request(request_data, i)
            print(response)

        print("done sending follower requests")

    def send_request_to_nodes_leader(self, data, function):
        for stub in self.client_for_nodes:
            print("stub")
            if function == 'create_buyer':
                print("CREATING BUYER VIA CLONE NODE GRPC")
                request_data = customer_service_pb2.ServerCreateBuyerRequest(username=data['username'], password=data['password'])
                try:
                    response = self.client_for_nodes[stub].ServerCreateBuyer(request_data)
                except Exception as e:
                    self.global_seq_number -= 1
                    print(e)

            if function == 'create_cart':
                print("CREATING CART VIA CLONE NODE GRPC")
                request_data = customer_service_pb2.CreateCartRequest(
                    item_name=data['item_name'],
                    item_id=data['item_id'],
                    buyer_id=data['buyer_id'],
                    quantity=data['quantity'],
                    price=data['price'],
                )
                response = self.client_for_nodes[stub].ServerCreateCart(request_data)

            if function == 'delete_buyer':
                print("DELETING BUYER VIA CLONE NODE GRPC")
                request_data = customer_service_pb2.DeleteCartByBuyerIdRequest(buyer_id=data['buyer_id'])
                response = self.client_for_nodes[stub].ServerDeleteCartByBuyerId(request)

            if function == 'update_cart':
                print("UPDATING CART VIA CLONE NODE GRPC")
                print(data)
                request_data = customer_service_pb2.UpdateCartItemQuantityRequest(
                    item_id=data['item_id'][0],
                    buyer_id=data['buyer_id'],
                    quantity=data['quantity'],
                )
                response = self.client_for_nodes[stub].ServerUpdateCartItemQuantity(request_data)

            if function == 'remove_item':
                print("DELETING ITEM VIA CLONE NODE GRPC")
                print(data)
                request_data = customer_service_pb2.RemoveCartItemRequest(
                    item_id=data['item_id'][0],
                    buyer_id=data['buyer_id'],
                )
                response = self.client_for_nodes[stub].ServerRemoveCartItem(request_data)



    def setup_routes(self):
        @app.route('/sequence', methods=['POST'])
        def sequence():
            data = request.get_json()
            print("DATA::", data)
            path = data['path']
            body = data['data']
            print("GLOBAL SEQUENCE NUMBER", self.global_seq_number, "NODE ID::", self.node_id)
            print("number of nodes", self.nodes)
            print(self.global_seq_number % len(self.nodes), ':: is leader')
            if len(self.nodes) == 0 or self.global_seq_number % len(self.nodes) == self.node_id:
                print("NODE", self.node_id, "IS LEADER")
                self.send_request_to_nodes_leader(body, path)
            return {'received': True}

        @app.route('/heartbeat', methods=['GET'])
        def heartbeat():
            return {'healthy': True}


server_host = "localhost"
server_port = 4444
rotating_sequencer_server = RotatingSequencerServer(server_host, server_port)

def get_db_credentials():
    with open('./credentials.json') as credentials:
        return json.load(credentials)


dao = Dao(get_db_credentials())


# class RequestForwardingInterceptor(grpc.ServerInterceptor):
#     def __init__(self):
#         self.local_seq_number = 0
#         self.global_seq_number = 0
#         self.nodes = set()
#
#     def from_worker(self, handler_call_details):
#         servicer_context = handler_call_details.invocation_metadata["servicer_context"]
#         peer_info = servicer_context.peer()
#
#         # Extract the IP address from peer information
#         # Format is "ipv4:<ip>:<port>" or "ipv6:[<ip>]:<port>"
#         ip_address = peer_info.split(':')[1].strip('[]')
#         if ip_address not in self.nodes:
#             return False
#         return True
#
#     def intercept_service(self, continuation, handler_call_details):
#         self.local_seq_number += 1
#         method = handler_call_details.method
#         print(f"Request #{self.request_count}: Received call to {method}")
#         # Here you can add more specific logging if needed.
#
#         # Continue with the normal flow of handling the request.
#         if self.from_worker(handler_call_details):
#             return continuation(handler_call_details)
#         else:
#             requests.post


class CustomerServiceServicer(customer_service_pb2_grpc.CustomerServiceServicer):
    def CreateBuyer(self, request, context):
        try:
            # dao.create_buyer(request.username, request.password)
            username = request.username
            password = request.password
            rotating_sequencer_server.send_request_to_nodes_follower('create_buyer',
                                                                     {'username': username,
                                                                              'password': password})

            print("sent request to followers")
            print()
            return customer_service_pb2.CreateBuyerResponse(success=True)
        except Exception as e:
            print(e)
            raise e

    def ServerCreateBuyer(self, request, context):
        print("In ServerCreateBuyer")
        rotating_sequencer_server.global_seq_number += 1
        dao.create_buyer(request.username, request.password)
        return customer_service_pb2.ServerCreateBuyerResponse(success=True)

    def GetBuyerId(self, request, context):
        return customer_service_pb2.GetBuyerIdResponse(buyer_id=dao.get_buyer_id(request.username, request.password))

    def CreateCart(self, request, context):
        item_name = request.item_name
        item_id = request.item_id
        buyer_id = request.buyer_id
        quantity = request.quantity
        price = request.price

        print('follower request:: about to add item to cart ')

        rotating_sequencer_server.send_request_to_nodes_follower('create_cart',
                                                                 {'item_name': item_name,
                                                                  'item_id': item_id,
                                                                  'buyer_id': buyer_id,
                                                                  'quantity':quantity,
                                                                  'price': price})

        return customer_service_pb2.CreateCartResponse(success=True)
        # dao.create_cart(request.item_name, request.item_id,
        #                         request.buyer_id, request.quantity,
        #                         request.price))

    def ServerCreateCart(self, request, context):
        rotating_sequencer_server.global_seq_number += 1
        dao.create_cart(request.item_name, request.item_id,
                                 request.buyer_id, request.quantity,
                                 request.price)

        return customer_service_pb2.CreateCartResponse(success=True)


    def DeleteCartByBuyerId(self, request, context):
        buyer_id = request.buyer_id
        rotating_sequencer_server.send_request_to_nodes_follower('delete_buyer',{'buyer_id': buyer_id})
        return customer_service_pb2.DeleteCartByBuyerIdResponse(success=True)

    def ServerDeleteCartByBuyerId(self, request, context):
        rotating_sequencer_server.global_seq_number += 1
        dao.delete_cart_by_buyer_id(request.buyer_id)
        return customer_service_pb2.DeleteCartByBuyerIdResponse(
            success=True)  #

    def GetCartItem(self, request, context):
        print("going to dao")
        db_item = dao.get_cart_item(request.item_id, request.buyer_id)
        if not db_item:
            print("no item found")
            return customer_service_pb2.GetCartItemResponse(item=customer_service_pb2.Item(
                id=-1,
                buyer_id=-1,
                item_id=-1,
                quantity=-1,
                price=-1)
            )

        print('get cart item final')
        print(db_item, type(db_item))
        cart_id = db_item[0]
        # cart_id = cart_id[0]
        print(cart_id, type(cart_id))
        buyer_id = db_item[1]
        # buyer_id = buyer_id[0]
        print(buyer_id, type(buyer_id))
        item_id = db_item[2]
        # item_id = item_id[0]
        print(item_id, type(item_id))
        quantity = db_item[3]
        # quantity = quantity[0]
        print(quantity, type(quantity))
        price = db_item[4]
        # price = price[0]
        print(price, type(price))
        item = customer_service_pb2.Item(
            id=cart_id,
            buyer_id=buyer_id,
            item_id=item_id,
            quantity=quantity,
            price=price,
        )
        print(item)
        return customer_service_pb2.GetCartItemResponse(item=item)

    def UpdateCartItemQuantity(self, request, context):
        item_id = request.item_id,
        buyer_id = request.buyer_id
        quantity = request.quantity

        rotating_sequencer_server.send_request_to_nodes_follower('update_cart',
                                                                 {'item_id': item_id,
                                                                  'buyer_id': buyer_id,
                                                                  'quantity': quantity,})

        return customer_service_pb2.UpdateCartItemQuantityResponse(success=True)
        # dao.update_cart_item_quantity(
        #                               ,
        #                               ))

    def ServerUpdateCartItemQuantity(self, request, context):
        rotating_sequencer_server.global_seq_number += 1
        dao.update_cart_item_quantity(request.item_id, request.buyer_id, request.quantity)

        return customer_service_pb2.UpdateCartItemQuantityResponse(success=True)

    def RemoveCartItem(self, request, context):
        item_id = request.item_id
        buyer_id = request.buyer_id
        rotating_sequencer_server.send_request_to_nodes_follower('remove_item',
                                                                 {'item_id': item_id,
                                                                  'buyer_id': buyer_id,})

        return customer_service_pb2.RemoveCartItemResponse(success=True)  # , dao.remove_cart_item(request.item_id,
        #               request.buyer_id))

    def ServerRemoveCartItem(self, request, context):
        rotating_sequencer_server.global_seq_number += 1
        dao.remove_cart_item(request.item_id, request.buyer_id)
        return customer_service_pb2.RemoveCartItemResponse(success=True)  # ,

    def GetBuyerCartItems(self, request, context):
        db_items = dao.get_buyer_cart_items(request.buyer_id)
        response = customer_service_pb2.GetBuyerCartItemsResponse()
        for db_item in db_items:
            print(db_item, type(db_item))
            cart_id = db_item[0]
            print(cart_id, type(cart_id))
            buyer_id = db_item[1]
            print(buyer_id, type(buyer_id))
            item_id = db_item[2]
            print(item_id, type(item_id))
            quantity = db_item[3]
            print(quantity, type(quantity))
            price = db_item[4]
            print(price, type(price))
            item = customer_service_pb2.Item(
                id=cart_id,
                buyer_id=buyer_id,
                item_id=item_id,
                quantity=quantity,
                price=price,
                name=db_item[5]
            )
            response.items.append(item)

        return response

    def GetBuyerPurchase(self, request, context):
        buyer_id = request.buyer_id
        db_items = dao.get_buyer_purchase(buyer_id)
        response = customer_service_pb2.GetBuyerPurchaseResponse()
        for db_item in db_items:
            print(db_item, type(db_item))
            cart_id = db_item[0]
            print(cart_id, type(cart_id))
            buyer_id = db_item[1]
            print(buyer_id, type(buyer_id))
            item_id = db_item[2]
            print(item_id, type(item_id))
            quantity = db_item[3]
            print(quantity, type(quantity))
            price = db_item[4]
            print(price, type(price))
            item = customer_service_pb2.Item(
                id=cart_id,
                buyer_id=buyer_id,
                item_id=item_id,
                quantity=quantity,
                price=price,
                name=db_item[5]
            )
            response.items.append(item)
        return response


def serve():
    # interceptor = RequestForwardingInterceptor()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))  # , interceptors=[interceptor])
    customer_service_pb2_grpc.add_CustomerServiceServicer_to_server(CustomerServiceServicer(), server)
    server.add_insecure_port('[::]:8994')
    print('Starting server. Listening on port 8994.')
    thread = threading.Thread(target=rotating_sequencer_server.run)
    thread.start()

    server.start()
    server.wait_for_termination()


if __name__ == '__main__':

    serve()


