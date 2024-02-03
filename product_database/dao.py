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

    def get_seller_id(self, username, password):
        try:
            seller_id = None
            with self.connection.cursor() as cursor:
                insert_query = sql.SQL("SELECT id FROM seller where username = {} AND password = {};").format(
                    sql.Literal(username), sql.Literal(password)
                )
                cursor.execute(insert_query)
                seller_id = cursor.fetchone()
            self.connection.commit()
            if seller_id == None or len(seller_id) == 0:
                print("seller's credentials does not exist")
                return None
            else:
                print("seller's credentials exists")
                return seller_id[0]
        except Exception as e:
            print(f"Error: Unable to find seller's Credentials.\n{e}")
            self.connection.commit()
            raise e
        
    def create_seller(self, username, password):
        try:
            with self.connection.cursor() as cursor:
                insert_query = sql.SQL("INSERT INTO seller (username, password) VALUES ({}, {});").format(
                    sql.Literal(username), sql.Literal(password)
                )
                cursor.execute(insert_query)
            self.connection.commit()
            print("Seller Account created successfully.")

        except Exception as e:
            print(f"Error: Unable to create seller account.\n{e}")
            self.connection.commit()
            raise e

    def create_item(self, seller_id, quantity, price, description):
        try:
            with self.connection.cursor() as cursor:
                insert_query = sql.SQL(
                    "INSERT INTO item (seller_id,quantity,price,description) VALUES ({}, {}, {}, {});").format(
                    sql.Literal(seller_id), sql.Literal(quantity), sql.Literal(price), sql.Literal(description)
                )
                cursor.execute(insert_query)
            self.connection.commit()
            print("Item created successfully.")

        except Exception as e:
            print(f"Error: Unable to create Item.\n{e}")
            self.connection.commit()
            raise e

    def get_all_items(self):
        try:
            with self.connection.cursor() as cursor:
                insert_query = sql.SQL("SELECT * FROM item")
                cursor.execute(insert_query)
                item_list = cursor.fetchall()
            self.connection.commit()
            return item_list

        except Exception as e:
            print(f"Error: Unable to Fetch Items.\n{e}")
            self.connection.commit()
            raise e

    def get_item_by_id(self, item_id):
        try:
            with self.connection.cursor() as cursor:
                insert_query = sql.SQL("SELECT * FROM item where id = {};").format(sql.Literal(item_id))
                cursor.execute(insert_query)
                item = cursor.fetchall()[0]
                print(item)
            self.connection.commit()
            return item
        except Exception as e:
            print(f"Error: Unable to Fetch Item details.\n{e}")
            self.connection.commit()
            raise e
    

    def get_item_seller_id(self, item_id):
        try:
            with self.connection.cursor() as cursor:
                insert_query = sql.SQL("SELECT seller_id FROM item where id = {};").format(sql.Literal(item_id))
                cursor.execute(insert_query)
                item = cursor.fetchall()[0]
                print(item)
            self.connection.commit()
            return item
        except Exception as e:
            print(f"Error: Unable to Fetch Seller Id.\n{e}")
            self.connection.commit()
            raise e
    
    def update_item_rating(self, item_id, item_rating):
        try:
            with self.connection.cursor() as cursor:
                update_query = sql.SQL("UPDATE item SET rating = {}, WHERE id = {};").format(
                    sql.Literal(item_rating), sql.Literal(item_id)
                )
                cursor.execute(update_query)
            self.connection.commit()
            print("buyer updated successfully.")
        except Exception as e:
            print(f"Error: Unable to update buyer.\n{e}")


    def update_seller_rating(self, seller_id, item_rating):
        try:
            with self.connection.cursor() as cursor:
                update_query = sql.SQL("UPDATE seller SET rating = rating + {}, WHERE id = {};").format(
                    sql.Literal(item_rating), sql.Literal(seller_id)
                )
                cursor.execute(update_query)
            self.connection.commit()
            print("buyer updated successfully.")
        except Exception as e:
            print(f"Error: Unable to update buyer.\n{e}")


    def get_item_price(self, item_id):
        try:
            with self.connection.cursor() as cursor:
                insert_query = sql.SQL("SELECT price FROM item where id = {};").format(sql.Literal(item_id))
                cursor.execute(insert_query)
                item = cursor.fetchall()[0][0]
                print(item)
            self.connection.commit()
            return item
        except Exception as e:
            print(f"Error: Unable to Fetch Seller Id.\n{e}")
            self.connection.commit()
            raise e
        
    def get_seller_rating(self, seller_id):
        try:
            with self.connection.cursor() as cursor:
                insert_query = sql.SQL("SELECT rating FROM seller where id = {}").format(
                    sql.Literal(seller_id))
                cursor.execute(insert_query)
                rating = cursor.fetchall()[0][0]
            self.connection.commit()
            return rating

        except Exception as e:
            print(f"Error: Unable to Fetch Item From Cart.\n{e}")
            self.connection.commit()
            raise e