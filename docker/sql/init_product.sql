-- DROP TABLE IF EXISTS sellers,items ;

CREATE TABLE IF NOT EXISTS seller (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    rating  INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS item (
    name VARCHAR(32) NOT NULL,
    id SERIAL PRIMARY KEY,
    seller_id INTEGER,
    quantity INTEGER,
    price REAL,
    rating INTEGER DEFAULT 0,
    description TEXT,
    category INTEGER NOT NULL,
    FOREIGN KEY(seller_id) REFERENCES seller(id)
);
