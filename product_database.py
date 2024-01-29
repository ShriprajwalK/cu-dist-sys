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