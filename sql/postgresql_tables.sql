CREATE TABLE users
(
    user_id    SERIAL PRIMARY KEY,
    user_name  VARCHAR(255),
    user_email VARCHAR(255)
);

CREATE TABLE products
(
    product_id       SERIAL PRIMARY KEY,
    product_name     VARCHAR(255),
    product_category VARCHAR(255)
);

CREATE TABLE stores
(
    store_id       SERIAL PRIMARY KEY,
    store_name     VARCHAR(255),
    store_location VARCHAR(255)
);

CREATE TABLE purchases
(
    purchase_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    store_id INTEGER REFERENCES stores(store_id),
    purchase_date DATE
);

CREATE TABLE purchase_items (
    purchase_item_id SERIAL PRIMARY KEY,
    purchase_id INTEGER REFERENCES purchases(purchase_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER,
    price REAL
);
