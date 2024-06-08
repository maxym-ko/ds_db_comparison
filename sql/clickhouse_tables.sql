CREATE TABLE users
(
    user_id    UInt32,
    user_name  String,
    user_email String
)
ENGINE = MergeTree()
ORDER BY user_id;


CREATE TABLE products
(
    product_id       UInt32,
    product_name     String,
    product_category String
)
ENGINE = MergeTree()
ORDER BY product_id;


CREATE TABLE stores
(
    store_id       UInt32,
    store_name     String,
    store_location String
)
ENGINE = MergeTree()
ORDER BY store_id;


CREATE TABLE purchases
(
    purchase_id UInt32,
    user_id UInt32,
    store_id UInt32,
    purchase_date Date
)
ENGINE = MergeTree()
ORDER BY purchase_id;

CREATE TABLE purchase_items (
    purchase_item_id UInt32,
    purchase_id UInt32,
    product_id UInt32,
    quantity UInt32,
    price Float32
)
ENGINE = MergeTree()
ORDER BY purchase_item_id;
