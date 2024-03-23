from concurrent import futures
import grpc
import product_service_pb2
import product_service_pb2_grpc
from dao import Dao
import json


def get_db_credentials():
    with open('./credentials.json') as credentials:
        return json.load(credentials)


class ProductServiceServicer(product_service_pb2_grpc.ProductServiceServicer):

    def __init__(self):
        self.dao = Dao(get_db_credentials(), '0.0.0.0:6670', ['0.0.0.0:6667', '0.0.0.0:6668',
                                                              '0.0.0.0:6669', '0.0.0.0:6666'])

    def CreateSeller(self, request, context):
        # Dummy implementation - in a real scenario, you would interact with a database
        print(f"Creating seller with username: {request.username}")
        try:
            self.dao.create_seller(request.username, request.password)
            return product_service_pb2.CreateSellerResponse(is_created=True)
        except Exception as e:
            print(e)
            raise e

    def SellItem(self, request, context):
        # Log the request and return a dummy success response
        success = self.dao.sell_item(int(request.seller_id), request.name, request.category, request.keywords,
                                request.condition, float(request.price), int(request.quantity))
        return product_service_pb2.SellItemResponse(success=success)

    def GetSellerById(self, request, context):
        return product_service_pb2.GetSellerByIdResponse(
            seller_id=self.dao.get_seller_id(request.username, request.password))

    def GetAllItems(self, request, context):
        db_items = self.dao.get_items_for_seller(request.seller_id)
        response = product_service_pb2.GetAllItemsResponse()
        for db_item in db_items:
            db_item = tuple(db_item)
            print('db_item', db_item, type(db_item), tuple(db_item), db_item[1], type(db_item[1]))
            print("GOING OVER DB ITEM AND CONVERTING")
            item_id = db_item[1],
            item_id = item_id[0]
            print("id:", item_id, type(item_id))
            seller_id = db_item[2],
            seller_id = seller_id[0]
            print("seller_id:", seller_id, type(seller_id))
            name = db_item[0],
            name = name[0]
            print("name:", name, type(name))
            category = db_item[7],
            category = category[0],
            category = category[0]
            print("category:", category, type(category))
            keywords = db_item[6]
            keywords = ' '.join(keywords.split())
            print("keywords:", keywords, type(keywords))
            condition = db_item[6]
            condition = condition.split()[-1][0],
            condition = condition[0]
            print("condition:", condition, type(condition))
            price = db_item[4],
            price = price[0]
            print("price:", price, type(price))
            quantity = db_item[3],
            quantity = quantity[0]
            print("quantity:", quantity, type(quantity))
            rating = db_item[5],
            rating = rating[0]
            print("rating:", rating, type(rating))
            description = db_item[6]
            print("description:", description, type(description))
            item = product_service_pb2.Item(
                id=item_id,
                seller_id=seller_id,
                name=name,
                category=category,
                keywords=keywords,
                condition=condition,
                price=price,
                quantity=quantity,
                rating=rating,
                description=description,
            )
            response.items.append(item)
            print("DONE CONVERTING")

        print("ITEMS::::")
        print(db_items)
        return response

    def UpdatePrice(self, request, context):
        return product_service_pb2.UpdatePriceResponse(success=self.dao.update_price(request.item_id, request.price))

    def GetItemsForSeller(self, request, context):
        db_items = self.dao.get_items_for_seller(request.seller_id)
        response = product_service_pb2.GetItemsForSellerResponse()
        for db_item in db_items:
            db_item = tuple(db_item)
            print('db_item', db_item, type(db_item), tuple(db_item), db_item[1], type(db_item[1]))
            print("GOING OVER DB ITEM AND CONVERTING")
            item_id = db_item[1],
            item_id = item_id[0]
            print("id:", item_id, type(item_id))
            seller_id = db_item[2],
            seller_id = seller_id[0]
            print("seller_id:", seller_id, type(seller_id))
            name = db_item[0],
            name = name[0]
            print("name:", name, type(name))
            category = db_item[7],
            category = category[0],
            category = category[0]
            print("category:", category, type(category))
            keywords = db_item[6]
            keywords = ' '.join(keywords.split())
            print("keywords:", keywords, type(keywords))
            condition = db_item[6]
            condition = condition.split()[-1][0],
            condition = condition[0]
            print("condition:", condition, type(condition))
            price = db_item[4],
            price = price[0]
            print("price:", price, type(price))
            quantity = db_item[3],
            quantity = quantity[0]
            print("quantity:", quantity, type(quantity))
            rating = db_item[5],
            rating = rating[0]
            print("rating:", rating, type(rating))
            description = db_item[6]
            print("description:", description, type(description))
            item = product_service_pb2.Item(
                id=item_id,
                seller_id=seller_id,
                name=name,
                category=category,
                keywords=keywords,
                condition=condition,
                price=price,
                quantity=quantity,
                rating=rating,
                description=description,
            )
            response.items.append(item)
            print("DONE CONVERTING")

        print("ITEMS::::")
        print(db_items)
        return response

    def GetSellerRatingById(self, request, context):
        return product_service_pb2.GetSellerRatingByIdResponse(rating=self.dao.get_seller_rating(request.seller_id))

    def RemoveItem(self, request, context):
        return product_service_pb2.RemoveItemResponse(success=self.dao.remove_item(request.item_id, request.quantity))

    def UpdateItemRating(self, request, context):
        return product_service_pb2.UpdateItemRatingResponse(success=self.dao.update_item_rating(request.item_id))

    def UpdateSellerRating(self, request, context):
        return product_service_pb2.UpdateSellerRatingResponse(success=self.dao.update_seller_rating(request.seller_id,
                                                                                               request.item_rating))

    def GetItemById(self, request, context):
        db_item = self.dao.get_item_by_id(request.item_id)
        print("GOING OVER DB ITEM AND CONVERTING")
        item_id = db_item[1],
        item_id = item_id[0]
        print("id:", item_id, type(item_id))
        seller_id = db_item[2],
        seller_id = seller_id[0]
        print("seller_id:", seller_id, type(seller_id))
        name = db_item[0],
        name = name[0]
        print("name:", name, type(name))
        category = db_item[7],
        category = category[0],
        category = category[0]
        print("category:", category, type(category))
        keywords = db_item[6]
        keywords = ' '.join(keywords.split())
        print("keywords:", keywords, type(keywords))
        condition = db_item[6]
        condition = condition.split()[-1][0],
        condition = condition[0]
        print("condition:", condition, type(condition))
        price = db_item[4],
        price = price[0]
        print("price:", price, type(price))
        quantity = db_item[3],
        quantity = quantity[0]
        print("quantity:", quantity, type(quantity))
        rating = db_item[5],
        rating = rating[0]
        print("rating:", rating, type(rating))
        description = db_item[6]
        print("description:", description, type(description))
        item = product_service_pb2.Item(
            id=item_id,
            seller_id=seller_id,
            name=name,
            category=category,
            keywords=keywords,
            condition=condition,
            price=price,
            quantity=quantity,
            rating=rating,
            description=description,
        )
        return product_service_pb2.GetItemByIdResponse(items=item)

    def GetItemPrice(self, request, context):
        print('getting item price')
        return product_service_pb2.GetItemPriceResponse(price=self.dao.get_item_price(request.item_id))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    product_service_pb2_grpc.add_ProductServiceServicer_to_server(ProductServiceServicer(), server)
    server.add_insecure_port('[::]:9005')
    print('Starting server. Listening on port 9005.')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
