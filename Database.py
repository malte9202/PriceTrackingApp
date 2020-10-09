import mysql.connector as mysql  # import mysql connector for database connection
from Config import host, user, password, database  # import credentials from config file


# database class
class Database(object):
    def __init__(self) -> None:  # init function to create connection
        # enable connection with data from .env file
        self.db_connection = mysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        # set db cursor with buffered parameter
        self.db_cursor = self.db_connection.cursor(buffered=True)

    # function to execute migrations
    def execute_migration(self, migrations: dict) -> None:
        # create table for migrations
        self.db_cursor.execute('CREATE TABLE IF NOT EXISTS migrations '
                               '(id INT AUTO_INCREMENT PRIMARY KEY, '
                               'name VARCHAR(255), '
                               'executed BOOLEAN DEFAULT FALSE);')
        # iterate through migrations
        for migration in migrations:
            executed_migrations_raw = self.execute_query('SELECT name FROM migrations WHERE executed = 1;')
            executed_migrations = []
            for executed_migration in executed_migrations_raw:
                executed_migrations.append(executed_migration[0])
            # if migration is not executed -> execute
            if migration not in executed_migrations:
                self.db_cursor.execute('INSERT INTO migrations (name) VALUES (%s);', (migration,))
                self.db_cursor.execute(migrations[migration])
                self.db_connection.commit()
                self.db_cursor.execute('UPDATE migrations '
                                       'SET executed = 1 '
                                       'WHERE name = (%s);', (migration,))
                self.db_connection.commit()
            else:  # skip migrations that were already executed
                pass

    # function to insert new products
    def insert_product(self, name: str, price_threshold: float, url: str) -> None:
        insert_statement = 'INSERT INTO products (name, price_threshold, url) VALUES (%s, %s, %s);'
        self.db_cursor.execute(insert_statement, (name, price_threshold, url))
        self.db_connection.commit()

    # function to insert price
    def insert_price(self, product_id: int, price: float) -> None:
        insert_statement = 'INSERT INTO prices (product_id, price) VALUES (%s, %s);'
        self.db_cursor.execute(insert_statement, (product_id, price))
        self.db_connection.commit()

    # function to fetch url from products table
    def get_url(self, product_id: int) -> str:
        query = 'SELECT url FROM products WHERE id = %s;'
        self.db_cursor.execute(query, (product_id,))
        url = self.db_cursor.fetchone()[0]
        return url

    # function to fetch product_ids from products table
    def get_product_ids(self) -> list:
        query = 'SELECT id FROM products;'
        self.db_cursor.execute(query)
        product_ids = []
        for element in self.db_cursor.fetchall():
            product_ids.append(element[0])
        return product_ids

    # function to execute queries
    def execute_query(self, query: str) -> list:
        self.db_cursor.execute(query)
        result = self.db_cursor.fetchall()
        return result

    # function to delete products
    def delete_product(self, product_id: int) -> None:
        delete_statement = 'DELETE FROM products WHERE id = %s;'
        self.db_cursor.execute(delete_statement, (product_id,))
        self.db_connection.commit()

    # function to delete prices
    def delete_price(self, product_id: int) -> None:
        delete_statement = 'DELETE FROM prices WHERE product_id = %s;'
        self.db_cursor.execute(delete_statement, (product_id,))
        self.db_connection.commit()

    # function to drop table, required for unittest
    def drop_table(self, table_name: str) -> None:
        delete_statement = f'DROP TABLE {table_name};'
        self.db_cursor.execute(delete_statement)
        self.db_connection.commit()

    # function to delete migration, required for unittest
    def delete_migration(self, migration_id: int) -> None:
        test_database = Database()  # init db
        delete_statement = 'DELETE FROM migrations WHERE id = %s;'
        self.db_cursor.execute(delete_statement, (migration_id,))
        self.db_connection.commit()

    def __del__(self) -> None:
        self.db_connection.close()
