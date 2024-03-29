-- DROP TABLE IF EXISTS buyers,shopping_cart, purchases ;

CREATE TABLE IF NOT EXISTS buyer (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE IF NOT EXISTS shopping_cart (
    id SERIAL PRIMARY KEY,
    buyer_id INTEGER,
    item_id INTEGER,
    quantity INTEGER,
    price INTEGER,
    item_name VARCHAR(32),
    FOREIGN KEY(buyer_id) REFERENCES buyer(id)
    -- FOREIGN KEY(product_id) REFERENCES products(id)
);

CREATE TABLE IF NOT EXISTS purchase (
    id SERIAL PRIMARY KEY,
    buyer_id INTEGER,
    item_id INTEGER UNIQUE,
    quantity INTEGER,
    item_name VARCHAR(32),
    FOREIGN KEY(buyer_id) REFERENCES buyer(id)
    -- FOREIGN KEY(product_id) REFERENCES products(id)
);
