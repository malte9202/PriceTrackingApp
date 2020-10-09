from unittest import TestCase  # import unittest functions
from Database import Database  # import database class


class TestDatabase(TestCase):
    def test_execute_migration(self) -> None:
        test_database = Database()  # init db
        # dict with test migrations
        test_migrations = {
            'test_migration_0001': 'CREATE TABLE IF NOT EXISTS test_1 '
            '(id INT AUTO_INCREMENT PRIMARY KEY, '
            'test_column_1 VARCHAR(255),'
            'test_column_2 FLOAT, '
            'test_column_3 VARCHAR(255));',
            'test_migration_0002': 'CREATE TABLE IF NOT EXISTS test_2 '
            '(test_column_1 INT NOT NULL, '
            'test_column_2 FLOAT NOT NULL, '
            'test_column_3 TIMESTAMP DEFAULT CURRENT_TIMESTAMP);'
        }
        # execute the test migrations
        Database.execute_migration(test_database, test_migrations)
        # check if test tables were created
        test_query = 'SHOW TABLES;'
        self.assertIn(('test_1',), Database.execute_query(test_database, test_query))
        self.assertIn(('test_2',), Database.execute_query(test_database, test_query))
        # remove test data
        Database.drop_table(test_database, 'test_1')
        Database.drop_table(test_database, 'test_2')
        # remove test migrations
        migration_id_query = 'SELECT id FROM migrations WHERE name = \'test_migration_0001\';'
        migration_id = Database.execute_query(test_database, migration_id_query)
        Database.delete_migration(test_database, migration_id[0][0])
        migration_id_query = 'SELECT id FROM migrations WHERE name = \'test_migration_0002\';'
        migration_id = Database.execute_query(test_database, migration_id_query)
        Database.delete_migration(test_database, migration_id[0][0])

    def test_insert_product(self) -> None:
        test_database = Database()  # init db
        # insert test product
        Database.insert_product(test_database, 'test product', 99.99, 'https://testproducturl.com')
        test_query = 'SELECT url FROM products WHERE name = \'test product\';'
        # check if url is equal
        self.assertEqual([('https://testproducturl.com',)], Database.execute_query(test_database, test_query))
        # get id from database
        test_id = Database.execute_query(test_database, 'SELECT id FROM products WHERE name = \'test product\';')[0][0]
        # delete test product from database
        Database.delete_product(test_database, test_id)

    def test_insert_price(self) -> None:
        test_database = Database()  # init db
        # insert test product
        Database.insert_product(test_database, 'test price product', 99.99, 'https://testpriceurl.com')
        # get id of inserted product
        test_id = Database.execute_query(test_database,
                                         'SELECT id FROM products WHERE name = \'test price product\';')[0][0]
        # insert price
        Database.insert_price(test_database, test_id, 9999.99)
        test_query = f'SELECT price FROM prices WHERE product_id = {test_id};'
        # check if price fetched from db is equal to inserted price
        self.assertEqual([(9999.99,)], Database.execute_query(test_database, test_query))
        # delete test data
        Database.delete_price(test_database, test_id)
        Database.delete_product(test_database, test_id)

    def test_get_url(self) -> None:
        test_database = Database()  # init db
        # insert test product
        Database.insert_product(test_database, 'test get url', 99.99, 'https://testgeturl.com')
        # get id of inserted test product
        test_id = Database.execute_query(test_database,
                                         'SELECT id FROM products WHERE name = \'test get url\';')[0][0]
        test_query = f'SELECT url FROM products WHERE id = {test_id};'
        # check if values are equal
        self.assertEqual([('https://testgeturl.com',)], Database.execute_query(test_database, test_query))
        Database.delete_product(test_database, test_id)  # delete test product

    def test_get_product_ids(self) -> None:
        test_database = Database()  # init db
        product_ids = Database.get_product_ids(test_database)  # fetch product_ids
        for product_id in product_ids:  # iterate through ids
            self.assertEqual(type(product_id), int)  # check if ids are integers

    def test_execute_query(self) -> None:
        test_database = Database()  # init db
        # get count result
        count_result = Database.execute_query(test_database, 'SELECT COUNT(id) FROM products;')[0][0]
        # check if count result returns integer
        self.assertEqual(type(count_result), int)
        # get list result
        list_result = Database.execute_query(test_database, 'SELECT * FROM prices;')
        # check if list result is list
        self.assertEqual(type(list_result), list)

    def test_delete_product(self) -> None:
        test_database = Database()  # init db
        # insert test product
        Database.insert_product(test_database, 'test delete', 99.99, 'https://testdelete.com')
        # get id of inserted product
        test_id = Database.execute_query(test_database, 'SELECT id FROM products WHERE name = \'test delete\';')[0][0]
        # delete product
        Database.delete_product(test_database, test_id)
        # test query to check if delete was successful
        test_result = Database.execute_query(test_database,
                                             'SELECT COUNT(1) FROM products WHERE name = \'test delete\';')[0][0]
        # check if product was deleted
        self.assertEqual(test_result, 0)

    def test_delete_price(self) -> None:
        test_database = Database()  # init db
        # insert test product
        Database.insert_product(test_database, 'test delete', 99.99, 'https://testdelete.com')
        # get id of test product
        test_id = Database.execute_query(test_database, 'SELECT id FROM products WHERE name = \'test delete\';')[0][0]
        # insert price for test product
        Database.insert_price(test_database, test_id, 777.77)
        # delete the price
        Database.delete_price(test_database, test_id)
        # test query
        test_result = Database.execute_query(test_database,
                                             f'SELECT COUNT(1) FROM prices WHERE product_id = {test_id};')[0][0]
        # check if the price was deleted
        self.assertEqual(test_result, 0)
        # delete test product
        Database.delete_product(test_database, test_id)

    def test_drop_table(self) -> None:
        test_database = Database()  # init db
        test_query = 'SHOW TABLES;'
        # check if tables from execute migration test where deleted
        self.assertNotIn(('test_1',), Database.execute_query(test_database, test_query))
        self.assertNotIn(('test_2',), Database.execute_query(test_database, test_query))

    def test_delete_migration(self) -> None:
        test_database = Database()
        test_query = 'SELECT name FROM migrations WHERE name IN (\'test_migration_0001\', \'test_migration_0002\');'
        self.assertNotIn('test_migration_0001', Database.execute_query(test_database, test_query))
        self.assertNotIn('test_migration_0002', Database.execute_query(test_database, test_query))


