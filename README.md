## Directory structure:
```
$ tree -I data
 .
└── ass1
    ├── README.md
    ├── buyer
    │   ├── Dockerfile
    │   ├── __init__.py
    │   ├── client_buyer.py
    │   ├── server_buyer.py
    │   └── server_buyer_helper.py
    ├── docker-compose.yaml
    ├── init_dbs.sh
    ├── postgres
    │   ├── __init__.py
    │   ├── credentials.json
    │   ├── customer_database.py
    │   └── product_database.py
    ├── seller
    │   ├── Dockerfile
    │   ├── __init__.py
    │   ├── client_seller.py
    │   ├── server_buyer.py
    │   ├── server_buyer_helper.py
    │   └── server_seller.py
    ├── sql
    │   ├── init_customer.sql
    │   └── init_product.sql
    └── todo.md   
```

## Instructions to run:
- `docker-compose up` to get postgresql up and running. init_customer and init_product scripts are run on startup(check docker-compose.yaml)
- Buyer server: Go to the parent of the ass1 directory and run: `python -m ass1.buyer.server_buyer`
- Buyer client: Go to the buyer directory and run: python client_buyer.py

