import psycopg2
from psycopg2 import sql

class CustomerDatabase:
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
            
        def create_buyer(self, username, password):
            try:
                with self.connection.cursor() as cursor:
                    insert_query = sql.SQL("INSERT INTO buyer (username, password) VALUES ({}, {});").format(
                        sql.Literal(username), sql.Literal(password)
                    )
                    cursor.execute(insert_query)
                self.connection.commit()
                print("Buyer Account created successfully.")

            except Exception as e:
                print(f"Error: Unable to create buyer.\n{e}")
                self.connection.commit()
                raise e
    

        def check_buyer_credentials(self, username, password):
            try:
                buyer_id = None
                with self.connection.cursor() as cursor:
                    insert_query = sql.SQL("SELECT id FROM buyer where username = {} AND password = {};").format(
                        sql.Literal(username), sql.Literal(password)
                    )
                    cursor.execute(insert_query)
                    buyer_id = cursor.fetchone()
                self.connection.commit()
                if(buyer_id==None or len(buyer_id)==0):
                    print("Buyer's credentials does not exist")
                    return None
                else:
                    print("Buyer's credentials exists")
                    return buyer_id[0]
            except Exception as e:
                print(f"Error: Unable to find Buyer's Credentials.\n{e}")
                self.connection.commit()
                raise e
            
        def get_buyer_id(self,username):
            try:
                with self.connection.cursor() as cursor:
                    select_query = sql.SQL("SELECT id FROM buyer where username = {};").format(sql.Literal(username))
                    cursor.execute(select_query)
                    buyer_id = cursor.fetchall()[0][0]
                self.connection.commit()
                return buyer_id
                
            except Exception as e:
                print(f"Error: Unable to Fetch Buyer Id.\n{e}")
                self.connection.commit()
                raise e
            

# def read_buyer_by_id(connection,):
#     try:
#         with self.connection.cursor() as cursor:
#             select_query = sql.SQL("SELECT * FROM buyers;")
#             cursor.execute(select_query)
#             buyers = cursor.fetchall()
#             for buyer in buyers:
#                 print(buyer)
#     except Exception as e:
#         print(f"Error: Unable to read buyers.\n{e}")

# # Function to update a buyer
# def update_buyer(connection, buyer_id, new_name, new_email):
#     try:
#         with self.connection.cursor() as cursor:
#             update_query = sql.SQL("UPDATE buyers SET name = {}, email = {} WHERE id = {};").format(
#                 sql.Literal(new_name), sql.Literal(new_email), sql.Literal(buyer_id)
#             )
#             cursor.execute(update_query)
#         self.connection.commit()
#         print("buyer updated successfully.")
#     except Exception as e:
#         print(f"Error: Unable to update buyer.\n{e}")

# # Function to delete a buyer
# def delete_buyer(connection, buyer_id):
#     try:
#         with self.connection.cursor() as cursor:
#             delete_query = sql.SQL("DELETE FROM buyers WHERE id = {};").format(sql.Literal(buyer_id))
#             cursor.execute(delete_query)
#         self.connection.commit()
#         print("buyer deleted successfully.")
#     except Exception as e:
#         print(f"Error: Unable to delete buyer.\n{e}")
    
# connection = connect()
# print(check_buyer_credentials(connection, "r", "r"))
# print(create_buyer(conn,"g","g"))
# # print(type(get_inserted_id(conn)))
            

# d = CustomerDatabase('customers','12345','localhost','5432','postgres')
# d.create_buyer("username","password")