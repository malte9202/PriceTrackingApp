from unittest import TestCase  # import unittest functions
from Database import Database  # import database class


class TestDatabase(TestCase):
    def test_execute_migration(self):
        pass

    def test_insert_product(self) -> None:
        test_database = Database()
        # insert test product
        Database.insert_product(test_database, 'test product', 99.99, 'https://testproducturl.com')
        test_query = 'SELECT url FROM products WHERE name = \'test product\';'
        # check if url is equal
        self.assertEqual([('https://testproducturl.com',)], Database.execute_query(test_database, test_query))
        # get id and delete the test product from database
        test_id = Database.execute_query(test_database, 'SELECT id FROM products WHERE name = \'test product\';')[0][0]
        Database.delete_product(test_database, test_id)

    def test_insert_price(self):
        pass

    def test_get_url(self):
        pass

    def test_get_product_ids(self):
        pass

    def test_execute_query(self):
        pass

    def test_delete_product(self):
        pass

    def test_delete_price(self):
        pass
