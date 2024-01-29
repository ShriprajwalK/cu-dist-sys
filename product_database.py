import psycopg2
from psycopg2 import sql

class ProductDatabase:
        def __init__(self, dbname,password,host,port,user):
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
                    insert_query = sql.SQL("INSERT INTO sellers (username, password) VALUES ({}, {});").format(
                        sql.Literal(username), sql.Literal(password)
                    )
                    cursor.execute(insert_query)
                self.connection.commit()
                print("Seller Account created successfully.")

            except Exception as e:
                print(f"Error: Unable to create seller account.\n{e}")
                self.connection.commit()
                raise e
            
        def create_item(self, seller_id,quantity,price,description ):
            try:
                with self.connection.cursor() as cursor:
                    insert_query = sql.SQL("INSERT INTO items (seller_id,quantity,price,description) VALUES ({}, {}, {}, {});").format(
                        sql.Literal(seller_id), sql.Literal(quantity), sql.Literal(price), sql.Literal(description)
                    )
                    cursor.execute(insert_query)
                self.connection.commit()
                print("Item created successfully.")

            except Exception as e:
                print(f"Error: Unable to create Item.\n{e}")
                self.connection.commit()
                raise e


# d = ProductDatabase('products','12345','localhost','5432','postgres')
# d.database_init("init_product.sql")
# d.create_seller("1","1")
# d.create_item(1 ,5,200,"orange, orange, round, fruit")