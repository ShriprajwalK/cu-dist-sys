import psycopg2
from psycopg2 import sql

db_params = {
    'dbname': 'customers',
    'password': '12345',
    'host': 'localhost',
    'port': '5432',
    'user': 'postgres'
}

def connect():
    try:
        connection = psycopg2.connect(**db_params)
        return connection
    except Exception as e:
        print(f"Error: Unable to connect to the database.\n{e}")
        return None

def create_buyer(connection, username, password):
    try:
        with connection.cursor() as cursor:
            insert_query = sql.SQL("INSERT INTO buyers (username, password) VALUES ({}, {});").format(
                sql.Literal(username), sql.Literal(password)
            )
            cursor.execute(insert_query)
        connection.commit()
        print("Buyer Account created successfully.")

    except Exception as e:
        print(f"Error: Unable to create buyer.\n{e}")
        connection.commit()
        raise e
    

def check_buyer_credentials(connection, username, password):
    try:
        buyer_id = None
        with connection.cursor() as cursor:
            insert_query = sql.SQL("SELECT id FROM buyers where username = {} AND password = {};").format(
                sql.Literal(username), sql.Literal(password)
            )
            cursor.execute(insert_query)
            buyer_id = cursor.fetchone()
        connection.commit()
        if(buyer_id==None or len(buyer_id)==0):
            print("Buyer's credentials does not exist")
            return None
        else:
            print("Buyer's credentials exists")
            return buyer_id[0]
    except Exception as e:
        print(f"Error: Unable to find Buyer's Credentials.\n{e}")
        connection.commit()
        raise e
    
def get_buyer_id(connection,username):
    try:
        with connection.cursor() as cursor:
            insert_query = sql.SQL("SELECT id FROM buyers where username = {};").format(sql.Literal(username))
            cursor.execute(insert_query)
            buyer_id = cursor.fetchall()[0][0]
        connection.commit()
        return buyer_id
        
    except Exception as e:
        print(f"Error: Unable to Fetch Buyer Id.\n{e}")
        connection.commit()
        raise e
        


# def read_buyer_by_id(connection,):
#     try:
#         with connection.cursor() as cursor:
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
#         with connection.cursor() as cursor:
#             update_query = sql.SQL("UPDATE buyers SET name = {}, email = {} WHERE id = {};").format(
#                 sql.Literal(new_name), sql.Literal(new_email), sql.Literal(buyer_id)
#             )
#             cursor.execute(update_query)
#         connection.commit()
#         print("buyer updated successfully.")
#     except Exception as e:
#         print(f"Error: Unable to update buyer.\n{e}")

# # Function to delete a buyer
# def delete_buyer(connection, buyer_id):
#     try:
#         with connection.cursor() as cursor:
#             delete_query = sql.SQL("DELETE FROM buyers WHERE id = {};").format(sql.Literal(buyer_id))
#             cursor.execute(delete_query)
#         connection.commit()
#         print("buyer deleted successfully.")
#     except Exception as e:
#         print(f"Error: Unable to delete buyer.\n{e}")
    
# connection = connect()
# print(check_buyer_credentials(connection, "r", "r"))
# print(create_buyer(conn,"g","g"))
# # print(type(get_inserted_id(conn)))