from unittest import TestCase  # import unittest functions
from Database import Database  # import database class


class TestDatabase(TestCase):
    def test_execute_migration(self):
        pass

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
        pass

    def test_delete_price(self) -> None:
        pass
