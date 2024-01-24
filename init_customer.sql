CREATE TABLE  IF NOT EXISTS buyers (
    id INTEGER PRIMARY KEY,
    username INTEGER PRIMARY KEY,
    password INTEGER PRIMARY KEY,
    age INTEGER
);

CREATE TABLE  IF NOT EXISTS shopping_cart (
    id INTEGER PRIMARY KEY,
    buyer_id INTEGER,
    product_id INTEGER,
    FOREIGN KEY(buyer_id) REFERENCES buyers(id)
    -- FOREIGN KEY(product_id) REFERENCES products(id)
);

CREATE TABLE  IF NOT EXISTS purchases (
    id INTEGER PRIMARY KEY,
    buyer_id INTEGER,
    product_id INTEGER,
    FOREIGN KEY(buyer_id) REFERENCES buyers(id)
    -- FOREIGN KEY(product_id) REFERENCES products(id)
);