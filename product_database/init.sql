-- DROP TABLE IF EXISTS sellers,items ;

CREATE TABLE IF NOT EXISTS seller (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    rating NUMERIC DEFAULT 0,
    items_sold INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS item (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER,
    quantity INTEGER,
    price NUMERIC,
    rating NUMERIC DEFAULT 0,
    description TEXT,
    FOREIGN KEY(seller_id) REFERENCES seller(id)
);
