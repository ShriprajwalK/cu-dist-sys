-- DROP TABLE IF EXISTS sellers,items ;

CREATE TABLE IF NOT EXISTS sellers (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    rating INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER,
    quantity INTEGER,
    price INTEGER,
    rating INTEGER DEFAULT 0,
    description TEXT,
    FOREIGN KEY(seller_id) REFERENCES sellers(id)
);