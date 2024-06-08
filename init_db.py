import psycopg2
from clickhouse_driver import Client

POSTGRESQL_TABLES_PATH = './sql/postgresql_tables.sql'
CLICKHOUSE_TABLES_PATH = './sql/clickhouse_tables.sql'


def init_postgres():
    conn = psycopg2.connect(dbname='purchases_db', host='localhost')
    cursor = conn.cursor()

    with open(POSTGRESQL_TABLES_PATH, 'r') as file:
        sql_script = file.read()
        cursor.execute(sql_script)
        conn.commit()

    cursor.close()
    conn.close()


def init_click_house():
    client = Client('localhost')

    with open(CLICKHOUSE_TABLES_PATH, 'r') as file:
        sql_statements = file.read()

    statements = [cmd.strip() for cmd in sql_statements.split(';') if cmd.strip()]

    for statement in statements:
        print(f"Executing: {statement}")
        client.execute(statement)


if __name__ == '__main__':
    init_postgres()
    init_click_house()
