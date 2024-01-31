import json
from .product_database import ProductDatabase
from .customer_database import CustomerDatabase


def get_db_credentials(db_name):
    with open(f'ass1/postgres/{db_name}_credentials.json') as credentials:
        return json.load(credentials)


def get_db(db_name):
    credentials = get_db_credentials(db_name)
    host = credentials['host']
    password = credentials['password']
    port = credentials['port']
    user = credentials['user']
    match db_name:
        case 'customer':
            return CustomerDatabase('customer', password, host, port, user)
        case 'product':
            return ProductDatabase('product', password, host, port, user)
