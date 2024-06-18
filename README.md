## Run Instructions

### Setting up ClickHouse (Column-Oriented Database)

#### Step 1: Download & Install ClickHouse
```shell
mkdir -p clickhouse
cd clickhouse
curl https://clickhouse.com/ | sh
```

#### Step 2: Start ClickHouse Server
```shell
cd clickhouse
./clickhouse server
```

### Setting up PostgreSQL (Relational Database)

#### Step 1: Start PostgreSQL
```shell
brew services start postgresql
```

#### Step 2: Create database
```shell
createdb purchases_db
```

### Populate both DB with fake data

#### Step 1: Create tables
```shell
pip install -r requirements.txt
python init_db.py
```

#### Step 2: (Optional) Clean tables
```shell
python clean_db.py
```

#### Step 3: Populate with fake data
```shell
python populate_db.py
```


### Analyze execution time

#### 1. Порахувати кількість проданового товару
* CLickHouse
```shell
cd clickhouse
./clickhouse client

SELECT SUM(quantity) AS total_sold_goods FROM purchase_items;
```
* PostgreSQL
```shell
psql purchases_db
\timing on

SELECT SUM(quantity) AS total_sold_goods FROM purchase_items;
```

#### 2. Порахувати вартість проданого товару
* CLickHouse
```shell
cd clickhouse
./clickhouse client

SELECT SUM(quantity * price) AS total_cost_of_sold_goods FROM purchase_items;
```
* PostgreSQL
```shell
psql purchases_db
\timing on

SELECT SUM(quantity * price) AS total_cost_of_sold_goods FROM purchase_items;
```

#### 3. Порахувати вартість проданого товару за період
* CLickHouse
```shell
cd clickhouse
./clickhouse client

SELECT SUM(quantity * price) AS total_cost_of_sold_goods
FROM purchase_items
JOIN purchases ON purchase_items.purchase_id = purchases.purchase_id
WHERE purchases.purchase_date BETWEEN '2024-04-01' AND '2024-08-31';
```
* PostgreSQL
```shell
psql purchases_db
\timing on

SELECT SUM(quantity * price) AS total_cost_of_sold_goods
FROM purchase_items
JOIN purchases ON purchase_items.purchase_id = purchases.purchase_id
WHERE purchases.purchase_date BETWEEN '2024-04-01' AND '2024-08-31';
```

#### 4. Порахувати скільки було придбано товару А в мазазині В за період С
* CLickHouse
```shell
cd clickhouse
./clickhouse client

SELECT SUM(quantity) AS total_quantity
FROM purchase_items
JOIN purchases ON purchase_items.purchase_id = purchases.purchase_id
WHERE purchase_items.product_id = 1 AND purchases.store_id = 2 AND purchases.purchase_date BETWEEN '2024-04-01' AND '2024-08-31';
```
* PostgreSQL
```shell
psql purchases_db
\timing on

SELECT SUM(quantity) AS total_quantity
FROM purchase_items
JOIN purchases ON purchase_items.purchase_id = purchases.purchase_id
WHERE purchase_items.product_id = 1 AND purchases.store_id = 2 AND purchases.purchase_date BETWEEN '2024-04-01' AND '2024-08-31';
```

#### 5. Порахувати скільки було придбано товару А в усіх магазинах за період С
* CLickHouse
```shell
cd clickhouse
./clickhouse client

SELECT SUM(quantity) AS total_quantity
FROM purchase_items
JOIN purchases ON purchase_items.purchase_id = purchases.purchase_id
WHERE purchase_items.product_id = 1 AND purchases.purchase_date BETWEEN '2024-04-01' AND '2024-08-31';
```
* PostgreSQL
```shell
psql purchases_db
\timing on

SELECT SUM(quantity) AS total_quantity
FROM purchase_items
JOIN purchases ON purchase_items.purchase_id = purchases.purchase_id
WHERE purchase_items.product_id = 1 AND purchases.purchase_date BETWEEN '2024-04-01' AND '2024-08-31';
```

#### 6. Порахувати сумарну виручку магазинів за період С
* CLickHouse
```shell
cd clickhouse
./clickhouse client

SELECT store_id, SUM(quantity * price) AS total_revenue
FROM purchase_items
JOIN purchases ON purchase_items.purchase_id = purchases.purchase_id
WHERE purchases.purchase_date BETWEEN '2024-04-01' AND '2024-08-31'
GROUP BY store_id;
```
* PostgreSQL
```shell
psql purchases_db
\timing on

SELECT store_id, SUM(quantity * price) AS total_revenue
FROM purchase_items
JOIN purchases ON purchase_items.purchase_id = purchases.purchase_id
WHERE purchases.purchase_date BETWEEN '2024-04-01' AND '2024-08-31'
GROUP BY store_id;
```

#### 7. Вивести топ 10 купівель товарів по два за період С (наприклад масло, хліб - 1000 разів)
* CLickHouse
```shell
cd clickhouse
./clickhouse client

SET allow_experimental_join_condition = 1;
```
```
WITH paired_purchases AS (
    SELECT a.purchase_id, a.product_id AS product1, b.product_id AS product2
    FROM purchase_items a
    INNER JOIN purchase_items b ON a.purchase_id = b.purchase_id AND a.product_id < b.product_id
    INNER JOIN purchases p ON a.purchase_id = p.purchase_id
    WHERE p.purchase_date BETWEEN '2024-04-01' AND '2024-08-31'
)
SELECT product1, product2, COUNT(*) AS count
FROM paired_purchases
GROUP BY product1, product2
ORDER BY count DESC
LIMIT 10;
```
* PostgreSQL
```shell
psql purchases_db
\timing on

WITH paired_purchases AS (
    SELECT a.product_id AS product1, b.product_id AS product2
    FROM purchase_items a
    JOIN purchase_items b ON a.purchase_id = b.purchase_id AND a.product_id < b.product_id
    JOIN purchases p ON a.purchase_id = p.purchase_id
    WHERE p.purchase_date BETWEEN '2024-04-01' AND '2024-08-31'
)
SELECT product1, product2, COUNT(*) AS count
FROM paired_purchases
GROUP BY product1, product2
ORDER BY count DESC
LIMIT 10;
```

#### 8. Вивести топ 10 купівель товарів по три за період С (наприклад молоко, масло, хліб - 1000 разів)
* CLickHouse
```shell
cd clickhouse
./clickhouse client

SET allow_experimental_join_condition = 1;
```
```
WITH trio_purchases AS (
    SELECT a.product_id AS product1, b.product_id AS product2, c.product_id AS product3
    FROM purchase_items a
    JOIN purchase_items b ON a.purchase_id = b.purchase_id AND a.product_id < b.product_id
    JOIN purchase_items c ON a.purchase_id = c.purchase_id AND b.product_id < c.product_id
    JOIN purchases p ON a.purchase_id = p.purchase_id
    WHERE p.purchase_date BETWEEN '2024-04-01' AND '2024-08-31'
)
SELECT product1, product2, product3, COUNT(*) AS count
FROM trio_purchases
GROUP BY product1, product2, product3
ORDER BY count DESC
LIMIT 10;
```
* PostgreSQL
```shell
psql purchases_db
\timing on

WITH trio_purchases AS (
    SELECT a.product_id AS product1, b.product_id AS product2, c.product_id AS product3
    FROM purchase_items a
    JOIN purchase_items b ON a.purchase_id = b.purchase_id AND a.product_id < b.product_id
    JOIN purchase_items c ON a.purchase_id = c.purchase_id AND b.product_id < c.product_id
    JOIN purchases p ON a.purchase_id = p.purchase_id
    WHERE p.purchase_date BETWEEN '2024-04-01' AND '2024-08-31'
)
SELECT product1, product2, product3, COUNT(*) AS count
FROM trio_purchases
GROUP BY product1, product2, product3
ORDER BY count DESC
LIMIT 10;
```

#### 9. Вивести топ 10 купівель товарів по чотири за період С
* CLickHouse
```shell
cd clickhouse
./clickhouse client

SET allow_experimental_join_condition = 1;
```
```
WITH quad_purchases as (
    SELECT a.product_id AS product1, b.product_id AS product2, c.product_id AS product3, d.product_id AS product4
    FROM purchase_items a
    INNER JOIN purchase_items b ON a.purchase_id = b.purchase_id AND a.product_id < b.product_id
    INNER JOIN purchase_items c ON a.purchase_id = c.purchase_id AND b.product_id < c.product_id
    INNER JOIN purchase_items d ON a.purchase_id = d.purchase_id AND c.product_id < d.product_id
    INNER JOIN purchases p ON a.purchase_id = p.purchase_id
    WHERE p.purchase_date BETWEEN '2024-04-01' AND '2024-08-31'
)
SELECT product1, product2, product3, product4, COUNT(*) AS count
FROM quad_purchases
GROUP BY product1, product2, product3, product4
ORDER BY count DESC
LIMIT 10;
```
* PostgreSQL
```shell
psql purchases_db
\timing on

WITH quad_purchases AS (
    SELECT a.product_id AS product1, b.product_id AS product2, c.product_id AS product3, d.product_id AS product4
    FROM purchase_items a
    JOIN purchase_items b ON a.purchase_id = b.purchase_id AND a.product_id < b.product_id
    JOIN purchase_items c ON a.purchase_id = c.purchase_id AND b.product_id < c.product_id
    JOIN purchase_items d ON a.purchase_id = d.purchase_id AND c.product_id < d.product_id
    JOIN purchases p ON a.purchase_id = p.purchase_id
    WHERE p.purchase_date BETWEEN '2024-04-01' AND '2024-08-31'
)
SELECT product1, product2, product3, product4, COUNT(*) AS count
FROM quad_purchases
GROUP BY product1, product2, product3, product4
ORDER BY count DESC
LIMIT 10;
```

### Cleaning up
```shell
dropdb purchases_db
brew services stop postgresql
```