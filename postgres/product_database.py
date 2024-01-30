import psycopg2
from psycopg2 import sql


class ProductDatabase:
    def __init__(self, dbname, password, host, port, user):
        self.db_params = {
            'dbname': dbname,
            'password': password,
            'host': host,
            'port': port,
            'user': user
        }
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

    def check_seller_credentials(self, username, password):
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
                print("Seller's credentials does not exist")
                return None
            else:
                print("Seller's credentials exists")
                return seller_id[0]
        except Exception as e:
            print(f"Error: Unable to find Seller's Credentials.\n{e}")
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
        # try:
        with self.connection.cursor() as cursor:
            insert_query = sql.SQL("SELECT * FROM item where id = {};").format(sql.Literal(item_id))
            cursor.execute(insert_query)
            item = cursor.fetchall()[0]
            print(item)
        self.connection.commit()
        return item

    # except Exception as e:
    #     print(f"Error: Unable to Fetch Buyer Id.\n{e}")
    #     self.connection.commit()
    #     raise e

# d = ProductDatabase('products','12345','localhost','5432','postgres')
# print(d.get_item_by_id(1))

# d.database_init("init_product.sql")
# d.create_seller("1","1")
# d.create_item(1 ,10,100,"apple, red, round, fruit")
# print(d.get_all_items())
