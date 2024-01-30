
class BuyerServerHelper:

    def __init__(self,customer_db, product_db):
        self.customer_db = customer_db
        self.product_db = product_db

    def choose_and_execute_action(self, action, data):
        response = {"action": action, "type": "buyer"}

        response_body = {}
        if(action=="create_account"):
            response_body = self.create_account(data)
        elif(action=="login"):
            response_body = self.login(data)
        elif(action=="search"):
            response_body = self.search(data)
        elif(action=="cart_add"):
            response_body = self.cart_add(data)

        response["body"] = response_body

        return response

    def login(self,data):
        username = data["body"]["username"]
        password = data["body"]["password"]
        response_body = {}
        try:
            buyer_id = self.customer_db.check_buyer_credentials(username,password)

            if(buyer_id!=None):
                response_body = {"login":True,"buyer_id" : buyer_id}
            else:
                response_body = {"login":False, "error":"Username/Password does not exist"}
        except Exception as e:
            response_body = {"login":False, "error":str(e)}

        return response_body

    def create_account(self, data):
        username = data["body"]["username"]
        password = data["body"]["password"]
        response_body = {}

        try:
            self.customer_db.create_buyer(username,password)
            response_body= {"is_created":True}
        except Exception as e:
            response_body = {"is_created":False, "error":str(e)}
        return response_body
    
    def jaccard_similarity(self,x,y):
        intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
        union_cardinality = len(set.union(*[set(x), set(y)]))
        return intersection_cardinality/float(union_cardinality)
    
    def search(self,data):
        item_keywords = data["body"]["keywords"]
        item_category = data["body"]["item_category"]
        comparing_text = item_keywords.join(item_category)
        response_body = {"items":[]}
        similarity_scores = []
        try:  
            item_list = self.product_db.get_all_items()
            for item in item_list:
                score = self.jaccard_similarity(comparing_text, item[5])
                similarity_scores.append((score, item))

            similarity_scores.sort(key=lambda k: k[0], reverse=True)
            items_list = [i[1] for i in similarity_scores]

            num_of_items = 5

            current_item_number = 1
            for ranked_item in item_list:
                item = {}
                item["item_id"] = ranked_item[0]
                item["quantity"] = ranked_item[2]
                item["price"] = ranked_item[3]
                item["rating"] = ranked_item[4]
                response_body["items"].append(item)
                current_item_number+=1
                if(current_item_number==num_of_items):
                    break
            
            return response_body
        except Exception as e:
            return response_body
        
    def cart_add(self,data):
        item_id = data["body"]["item_id"]
        requested_quantity = data["body"]["quantity"]
        response_body = {}

        try:
            item = self.product_db.get_item_by_id(item_id)
            available_quantity = item[2]
            price = item[3]
            if(requested_quantity>=available_quantity):
                return {"add":False, "Reason":"Requested Quantity Not Present in the Database"}

            item_details = [item_id, requested_quantity,price]

            response_body = {"add":True, "item_details":item_details}
            return response_body 
        except Exception as e:
            print(e)
            return {"add":False, "Reason":"Item Not Present in the Database"}





         

         