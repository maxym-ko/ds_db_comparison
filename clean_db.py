import psycopg2
from clickhouse_driver import Client


def clean_postgres():
    conn = psycopg2.connect(dbname='purchases_db', host='localhost')
    cursor = conn.cursor()

    print('Cleaning users...')
    cursor.execute('TRUNCATE TABLE users RESTART IDENTITY CASCADE')

    print('Cleaning products...')
    cursor.execute('TRUNCATE TABLE products RESTART IDENTITY CASCADE')

    print('Cleaning stores...')
    cursor.execute('TRUNCATE TABLE stores RESTART IDENTITY CASCADE')

    print('Cleaning purchases...')
    cursor.execute('TRUNCATE TABLE purchases RESTART IDENTITY CASCADE')

    print('Cleaning purchase_items...')
    cursor.execute('TRUNCATE TABLE purchase_items RESTART IDENTITY CASCADE')

    print('Committing...')
    conn.commit()
    cursor.close()
    conn.close()


def clean_click_house():
    client = Client('localhost')

    print('Cleaning users...')
    client.execute('TRUNCATE users')

    print('Cleaning products...')
    client.execute('TRUNCATE products')

    print('Cleaning stores...')
    client.execute('TRUNCATE stores')

    print('Cleaning purchases...')
    client.execute('TRUNCATE purchases')

    print('Cleaning purchase_items...')
    client.execute('TRUNCATE purchase_items')


if __name__ == '__main__':
    print('Cleaning `PostgreSQL`...')
    clean_postgres()

    print('Cleaning `ClickHouse`...')
    clean_click_house()

    print('Done')
