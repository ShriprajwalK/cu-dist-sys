import psycopg2
from psycopg2 import sql


class Dao:
    def __init__(self, db_params):
        self.db_params = db_params
        try:
            self.connection = psycopg2.connect(**self.db_params)
        except Exception as e:
            print(f"Error: Unable to connect to the database.\n{e}")
            raise e

    def database_init(self, sql_script):
        with self.connection.cursor() as cursor:
            cursor.execute(open(sql_script, "r").read())

        self.connection.commit()
        print("SQL script executed successfully.")

    def create_buyer(self, username, password):
        try:
            with self.connection.cursor() as cursor:
                insert_query = sql.SQL("INSERT INTO buyer (username, password) VALUES ({}, {});").format(
                    sql.Literal(username), sql.Literal(password)
                )
                cursor.execute(insert_query)
            self.connection.commit()
            print("Buyer Account created successfully.")
            return True

        except Exception as e:
            print(f"Error: Unable to create buyer.\n{e}")
            self.connection.commit()
            raise e

    def get_buyer_id(self, username, password):
        try:
            buyer_id = None
            with self.connection.cursor() as cursor:
                insert_query = sql.SQL("SELECT id FROM buyer where username = {} AND password = {};").format(
                    sql.Literal(username), sql.Literal(password)
                )
                cursor.execute(insert_query)
                buyer_id = cursor.fetchone()
            self.connection.commit()
            if buyer_id == None or len(buyer_id) == 0:
                print("Buyer's credentials does not exist")
                return None
            else:
                print("Buyer's credentials exists")
                return buyer_id[0]
        except Exception as e:
            print(f"Error: Unable to find Buyer's Credentials.\n{e}")
            self.connection.commit()
            raise e
        
    def get_buyer_purchase(self, buyer_id):
        try:
            with self.connection.cursor() as cursor:
                insert_query = sql.SQL("SELECT * FROM purchase where buyer_id = {}").format(
                    sql.Literal(buyer_id))
                cursor.execute(insert_query)
                item_list = cursor.fetchall()
            self.connection.commit()
            return item_list

        except Exception as e:
            print(f"Error: Unable to Fetch Items.\n{e}")
            self.connection.commit()
            raise e
        
    def create_cart(self,item_name, item_id,buyer_id, quantity,price):
        try:
            with self.connection.cursor() as cursor:
                insert_query = sql.SQL("INSERT INTO shopping_cart (buyer_id, item_id,quantity, price,item_name) VALUES ({}, {},{},{}, {});").format(
                    sql.Literal(buyer_id), sql.Literal(item_id), sql.Literal(quantity), sql.Literal(price), sql.Literal(item_name)
                )
                cursor.execute(insert_query)
            self.connection.commit()
            print("Added Item to Cart successfully.")
            return True

        except Exception as e:
            print(f"Error: Unable to Add to Cart.\n{e}")
            self.connection.commit()
            raise e
        
    def delete_cart_by_buyer_id(self, buyer_id):
        try:
            with self.connection.cursor() as cursor:
                insert_query = sql.SQL("DELETE FROM shopping_cart WHERE buyer_id = {};").format(
                    sql.Literal(buyer_id)
                )
                cursor.execute(insert_query)
            self.connection.commit()
            print("Deleted Items From Cart successfully.")
            return True

        except Exception as e:
            print(f"Error: Unable to Delete from Cart.\n{e}")
            self.connection.commit()
            raise e
        
    def get_cart_item(self, item_id, buyer_id):
        try:
            with self.connection.cursor() as cursor:
                insert_query = sql.SQL("SELECT * FROM shopping_cart where buyer_id = {} AND item_id = {}").format(
                    sql.Literal(buyer_id),sql.Literal(item_id))
                cursor.execute(insert_query)
                items = cursor.fetchall()
                print(items)
                if len(items) == 0:
                    return False
                return items[0]
            self.connection.commit()
            return item

        except Exception as e:
            print(f"Error: Unable to Fetch Item From Cart--> GET CART ITEM.\n{e}")
            print("BUYER ID: ", buyer_id, item_id)
            self.connection.commit()
            raise e
        
    def update_cart_item_quantity(self, item_id, buyer_id, quantity):
        try:
            with self.connection.cursor() as cursor:
                update_query = sql.SQL("UPDATE shopping_cart SET quantity = {} WHERE item_id = {} AND buyer_id = {};").format(
                    sql.Literal(quantity), sql.Literal(item_id), sql.Literal(buyer_id)
                )
                cursor.execute(update_query)
            self.connection.commit()
            print("Cart Item Quantity updated successfully.")
            return True
        except Exception as e:
            print(f"Error: Unable to update Cart Item's Quantity.\n{e}")


    def remove_cart_item(self, item_id, buyer_id):
        try:
            with self.connection.cursor() as cursor:
                insert_query = sql.SQL("DELETE FROM shopping_cart WHERE  buyer_id = {} AND item_id = {};").format(
                    sql.Literal(buyer_id), sql.Literal(item_id)
                )
                cursor.execute(insert_query)
            self.connection.commit()
            print("Deleted Item From Cart successfully.")
            return True

        except Exception as e:
            print(f"Error: Unable to Delete Item from Cart.\n{e}")
            self.connection.commit()
            raise e
        
    def get_buyer_cart_items(self, buyer_id):
        try:
            print("SELECT * FROM shopping_cart where buyer_id =")
            with self.connection.cursor() as cursor:
                insert_query = sql.SQL("SELECT * FROM shopping_cart where buyer_id = {}").format(
                    sql.Literal(buyer_id))
                cursor.execute(insert_query)
                items = cursor.fetchall()
            self.connection.commit()
            return items

        except Exception as e:
            print(f"Error: Unable to Fetch Item From Cart --> BUYER CART ITEMS\n{e}")
            print(buyer_id)
            self.connection.commit()
            raise e


