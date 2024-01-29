-- DROP TABLE IF EXISTS buyers,shopping_cart, purchases ;

CREATE TABLE IF NOT EXISTS buyers (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE IF NOT EXISTS shopping_cart (
    id SERIAL PRIMARY KEY,
    buyer_id INTEGER,
    item_id INTEGER UNIQUE,
    FOREIGN KEY(buyer_id) REFERENCES buyers(id)
    -- FOREIGN KEY(product_id) REFERENCES products(id)
);

CREATE TABLE IF NOT EXISTS purchases (
    id SERIAL PRIMARY KEY,
    buyer_id INTEGER,
    item_id INTEGER UNIQUE,
    FOREIGN KEY(buyer_id) REFERENCES buyers(id)
    -- FOREIGN KEY(product_id) REFERENCES products(id)
);