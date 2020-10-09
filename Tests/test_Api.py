from unittest import TestCase
from Api import ProductList, CreateProduct, Product, Price


class TestProductList(TestCase):
    def test_get(self):
        self.assertEqual(type(ProductList.get()), list, msg='function should return list')


class TestCreateProduct(TestCase):
    def test_post(self):
        pass

class TestProduct(TestCase):
    def test_get(self):
        pass

    def test_delete(self):
        pass


class TestPrice(TestCase):
    def test_get(self):
        pass


class TestEndpoints(TestCase):
    def test_productlist(self):
        pass

    def test_product(self):
        pass

    def test_price(self):
        pass

    def test_createproduct(self):
        pass
