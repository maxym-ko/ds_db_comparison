import psycopg2
from clickhouse_driver import Client
from faker import Faker
import random


def generate_fake_data():
    fake = Faker()

    print(f'Generating samples of fake data...')
    users = [(i, fake.name(), fake.email()) for i in range(1, 2_000)]
    products = [(i, fake.word(), fake.word()) for i in range(1, 1_000)]
    stores = [(i, fake.company(), fake.city()) for i in range(1, 50)]
    purchases = [(i, fake.random_element(users)[0], fake.random_element(stores)[0], fake.date_this_year())
                 for i in range(1, 200_000)]

    # Generate purchase items and aggregate them by product_id within each purchase
    purchase_items_dict = {}
    for purchase_id, user_id, store_id, purchase_date in purchases:
        num_items = random.randint(1, 10)
        for _ in range(num_items):
            product_id = fake.random_element(products)[0]
            quantity = fake.random_int(min=1, max=10)
            price = round(random.uniform(10.0, 100.0), 2)
            if (purchase_id, product_id) in purchase_items_dict:
                purchase_items_dict[(purchase_id, product_id)]['quantity'] += quantity
                purchase_items_dict[(purchase_id, product_id)]['price'] = price  # Update price to latest one
            else:
                purchase_items_dict[(purchase_id, product_id)] = {'quantity': quantity, 'price': price}

    # Convert the dictionary to a list for insertion
    purchase_items = [(purchase_id, product_id, data['quantity'], data['price']) for (purchase_id, product_id), data in
                      purchase_items_dict.items()]

    return users, products, stores, purchases, purchase_items


def populate_postgres(users, products, stores, purchases, purchase_items):
    conn = psycopg2.connect(dbname='purchases_db', host='localhost')
    cursor = conn.cursor()

    print('Inserting into users...')
    cursor.executemany('INSERT INTO users (user_name, user_email) VALUES (%s, %s)',
                       [(name, email) for _, name, email in users])

    print('Inserting into products...')
    cursor.executemany('INSERT INTO products (product_name, product_category) VALUES (%s, %s)',
                       [(name, category) for _, name, category in products])

    print('Inserting into stores...')
    cursor.executemany('INSERT INTO stores (store_name, store_location) VALUES (%s, %s)',
                       [(name, location) for _, name, location in stores])

    print('Inserting into purchases...')
    cursor.executemany('INSERT INTO purchases (user_id, store_id, purchase_date) VALUES (%s, %s, %s)',
                    [(user_id, store_id, purchase_date) for _, user_id, store_id, purchase_date in purchases])

    print('Inserting into purchase_items...')
    cursor.executemany('INSERT INTO purchase_items (purchase_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)',
                       purchase_items)

    print('Committing...')
    conn.commit()
    cursor.close()
    conn.close()


def populate_click_house(users, products, stores, purchases, purchase_items):
    client = Client('localhost')

    print('Inserting into users...')
    client.execute('INSERT INTO users (user_id, user_name, user_email) VALUES', users)

    print('Inserting into products...')
    client.execute('INSERT INTO products (product_id, product_name, product_category) VALUES', products)

    print('Inserting into stores...')
    client.execute('INSERT INTO stores (store_id, store_name, store_location) VALUES', stores)

    print('Inserting into purchases...')
    client.execute('INSERT INTO purchases (purchase_id, user_id, store_id, purchase_date) VALUES', purchases)

    print('Inserting into purchase_items...')
    client.execute('INSERT INTO purchase_items (purchase_id, product_id, quantity, price) VALUES', purchase_items)


if __name__ == '__main__':
    fake_users, fake_products, fake_stores, fake_purchases, fake_purchase_items = generate_fake_data()

    print('Populating `PostgreSQL`...')
    populate_postgres(fake_users, fake_products, fake_stores, fake_purchases, fake_purchase_items)

    print('Populating `ClickHouse`...')
    populate_click_house(fake_users, fake_products, fake_stores, fake_purchases, fake_purchase_items)

    print('Done')
