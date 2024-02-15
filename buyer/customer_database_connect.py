import socket
import json
import grpc
import customer_service_pb2
import customer_service_pb2_grpc
from google.protobuf.json_format import MessageToDict

class CustomerDatabaseConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.url = str(self.host) + ":" + str(self.port)
        self.stub = customer_service_pb2_grpc.CustomerServiceStub(grpc.insecure_channel(self.url))

    def send_request(self, request):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(json.dumps(request).encode('utf-8'))
            response = s.recv(1024).decode('utf-8')
            return json.loads(response)

    def get_buyer_by_id(self, username, password):
        request = customer_service_pb2.GetBuyerIdRequest(username=username, password=password)
        response = self.stub.GetBuyerId(request)
        return response.buyer_id

    def create_buyer(self, username, password):
        request = customer_service_pb2.CreateBuyerRequest(username=username, password=password)
        response = self.stub.CreateBuyer(request)
        return response.is_created

    def get_purchase_history(self, buyer_id):
        request = customer_service_pb2.GetBuyerPurchaseRequest(buyer_id=buyer_id)
        response = self.stub.GetBuyerPurchase(request)
        return response.items

    def add_to_cart(self, item_name, item_id, buyer_id, quantity, price):
        request = customer_service_pb2.CreateCartRequest(
            item_name=item_name,
            item_id=item_id,
            buyer_id=buyer_id,
            quantity=quantity,
            price=price,
        )
        response = self.stub.CreateCart(request)
        return response.success

    def delete_cart_by_buyer_id(self, buyer_id):
        request = customer_service_pb2.DeleteCartByBuyerIdRequest(buyer_id=buyer_id)
        response = self.stub.DeleteCartByBuyerId(request)
        return response.success

    def remove_cart_item(self, item_id, buyer_id):
        request = customer_service_pb2.RemoveCartItemRequest(item_id=item_id, buyer_id=buyer_id)
        response = self.stub.RemoveCartItem(request)
        return response.success

    def get_cart_item(self, item_id, buyer_id):
        request = customer_service_pb2.GetCartItemRequest(item_id=item_id, buyer_id=buyer_id)
        print('before rpc')
        response = self.stub.GetCartItem(request)
        print('after rpc')
        item = MessageToDict(response.item, preserving_proto_field_name=True)
        if item['item_id'] == -1:
            return None
        return item

    def update_cart_item_quantity(self, item_id, buyer_id, quantity):
        request = customer_service_pb2.UpdateCartItemQuantityRequest(item_id=item_id, buyer_id=buyer_id,
                                                                     quantity=quantity)
        response = self.stub.UpdateCartItemQuantity(request)
        return response.success

    def get_buyer_cart_items(self, buyer_id):
        request = customer_service_pb2.GetBuyerCartItemsRequest(buyer_id=buyer_id)
        response = self.stub.GetBuyerCartItems(request)
        items = [MessageToDict(item, preserving_proto_field_name=True) for item in response.items]
        print("ITEMS IN CART", items)
        return items
