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
    │   └── sessions_manager.py
    |
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
    │   └── sessions_manager.py
    ├── sql
    │   ├── init_customer.sql
    │   └── init_product.sql
    └── todo.md   
```

## Instructions to run:
- `docker-compose up` to get postgresql up and running. init_customer and init_product scripts are run on startup(check docker-compose.yaml)
The system comprises of 6 components:
- Buyer server: Go to the parent of the directory and run: `python -m buyer.server_buyer`
- Seller server: Go to the parent of the directory and run: `python -m seller.server_seller`
- Buyer client: Go to the buyer directory and run: `python client_buyer.client_buyer.py`
- Seller client: Go to the buyer directory and run: `python seller_buyer.seller_buyer.py`
- Customer Database: Go to the buyer directory and run: `python customer_database.server.py`
- Product Database: Go to the buyer directory and run: `python product_database.server.py`

System Design - The 6 components are running on separate servers to simulate a distributed systems environment. The code is written in python. REST API is implemented for communicating between the client and the server. gRPC is implemented for communication between server and database. PostgreSQL is implemented for the database backend. The server uses SOAP to communicate with the financial transcations. The servers and the databases are hosted on the GCPcloud.Also the client side is stateless frontend design, where state information is maintained in the backend databases.

Current State of the System - All the APIs for seller and buyer are working as stated in this assignment. The Finance transaction is operational right now. It also includes the purchases API done by the buyer to purchase items from the saved cart.

Assumptions - The password for client and seller is plain text. Currently no security measures are taken like authentication mechanisms to ensure secure transfer of data between the client and the server. None of the data is stored on the server as cache. Therefore if the database stops responding, the server will not recvieve any data to process client's request and the entire system will crash.



