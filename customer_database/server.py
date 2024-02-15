import socket
import sys
import json
from concurrent import futures
import grpc
import customer_service_pb2
import customer_service_pb2_grpc
from dao import Dao
from server_helper import ServerHelper

def get_db_credentials():
    with open('./credentials.json') as credentials:
        return json.load(credentials)


dao = Dao(get_db_credentials())

class CustomerServiceServicer(customer_service_pb2_grpc.CustomerServiceServicer):
    def CreateBuyer(self, request, context):
        try:
            dao.create_buyer(request.username, request.password)
            return customer_service_pb2.CreateBuyerResponse(success=True)
        except Exception as e:
            print(e)
            raise e
        pass

    def GetBuyerId(self, request, context):
        return customer_service_pb2.GetBuyerIdResponse(buyer_id=dao.get_buyer_id(request.username, request.password))

    def CreateCart(self, request, context):
        return customer_service_pb2.CreateCartResponse(success=dao.create_cart(request.item_name, request.item_id,
                                                                               request.buyer_id, request.quantity,
                                                                               request.price))

    def DeleteCartByBuyerId(self, request, context):
        return customer_service_pb2.DeleteCartByBuyerIdResponse(success=dao.delete_cart_by_buyer_id(request.buyer_id))

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
        #cart_id = cart_id[0]
        print(cart_id, type(cart_id))
        buyer_id = db_item[1]
        #buyer_id = buyer_id[0]
        print(buyer_id, type(buyer_id))
        item_id = db_item[2]
        #item_id = item_id[0]
        print(item_id, type(item_id))
        quantity = db_item[3]
        #quantity = quantity[0]
        print(quantity, type(quantity))
        price = db_item[4]
        #price = price[0]
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
        return customer_service_pb2.UpdateCartItemQuantityResponse(success=
                                                                   dao.update_cart_item_quantity(request.item_id,
                                                                                                 request.buyer_id,
                                                                                                 request.quantity))

    def RemoveCartItem(self, request, context):
        return customer_service_pb2.RemoveCartItemResponse(success=dao.remove_cart_item(request.item_id,
                                                                                        request.buyer_id))

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
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    customer_service_pb2_grpc.add_CustomerServiceServicer_to_server(CustomerServiceServicer(), server)
    server.add_insecure_port('[::]:9000')
    print('Starting server. Listening on port 9000.')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
