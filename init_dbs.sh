#!/bin/bash
set -e

# Create the databases
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE customer;
    CREATE DATABASE product;
EOSQL

# Initialize each database using its own SQL script
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "customer" -f /sql/init_customer.sql
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "product" -f /sql/init_product.sql
