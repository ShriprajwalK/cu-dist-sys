import grpc
import product_service_pb2
import product_service_pb2_grpc
from google.protobuf.json_format import MessageToDict


class ProductDatabaseConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.url = str(self.host) + ":" + str(self.port)
        self.stub = product_service_pb2_grpc.ProductServiceStub(grpc.insecure_channel(self.url))

    def get_seller_by_id(self, username, password):
        request = product_service_pb2.GetSellerByIdRequest(username=username, password=password)
        response = self.stub.GetSellerById(request)
        print("RESPONSE", response, "RESPONSE.SELLER_ID", response.seller_id)
        return response.seller_id

    def create_seller(self, username, password):
        request = product_service_pb2.CreateSellerRequest(username=username, password=password)
        response = self.stub.CreateSeller(request)
        return response.is_created

    def get_all_items(self):
        request = product_service_pb2.GetAllItemsRequest()
        response = self.stub.GetAllItems(request)
        return response.items

    def get_seller_rating_by_id(self, seller_id):
        request = product_service_pb2.GetSellerRatingByIdRequest(seller_id=seller_id)
        response = self.stub.GetSellerRatingById(request)
        return response.rating

    def sell_item(self, seller, name, category, keywords, condition, price, quantity):
        print("---SELL", seller, type(seller))
        print(quantity, type(quantity))
        request = product_service_pb2.SellItemRequest(seller_id=int(seller), name=name, category=category,
                                                      keywords=keywords,condition=condition, price=float(price),
                                                      quantity=int(quantity))
        response = self.stub.SellItem(request)
        return response.success

    def update_price(self, item_id, price):
        request = product_service_pb2.UpdatePriceRequest(item_id=int(item_id), price=int(price))
        response = self.stub.UpdatePrice(request)
        return response.success

    def remove_item(self, item_id, quantity):
        request = product_service_pb2.RemoveItemRequest(item_id=int(item_id), quantity=int(quantity))
        response = self.stub.RemoveItem(request)
        return response.success

    def get_items_for_seller(self, seller_id):
        request = product_service_pb2.GetItemsForSellerRequest(seller_id=seller_id)
        response = self.stub.GetItemsForSeller(request)
        items_list = [MessageToDict(item, preserving_proto_field_name=True) for item in response.items]
        return items_list

    def get_seller_rating(self, seller_id):
        request = product_service_pb2.GetSellerRatingByIdRequest(seller_id=seller_id)
        response = self.stub.GetSellerRatingById(request)
        return response.rating

    def get_item_price(self, item_id):
        request = product_service_pb2.GetItemPriceRequest(item_id=int(item_id))
        response = self.stub.GetItemPrice(request)
        return response.price

    def update_seller_rating(self, seller_id, item_rating):
        request = product_service_pb2.UpdateSellerRatingRequest(seller_id=int(seller_id), item_rating=int(item_rating))
        response = self.stub.UpdateSellerRating(request)
        return response.success

    def get_item_by_id(self, item_id):
        request = product_service_pb2.GetItemByIdRequest(item_id=int(item_id))
        response = self.stub.GetItemById(request)
        print(response.items,MessageToDict(response.items, preserving_proto_field_name=True))
        return MessageToDict(response.items, preserving_proto_field_name=True)

    def get_item_seller_id(self, item_id):
        request = product_service_pb2.GetItemSellerIdRequest(item_id=int(item_id))
        response = self.stub.GetItemSellerId(request)
        return response.seller_id

    def update_item_rating(self, item_id, item_rating):
        request = product_service_pb2.UpdateItemRatingRequest(item_id=int(item_id), item_rating=int(item_rating))
        response = self.stub.UpdateItemRating(request)
        return response.success
