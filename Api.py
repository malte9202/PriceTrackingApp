# import required flask extensions
from flask import Flask
from flask_restful import reqparse, Api, Resource
# import Database class
from Database import Database

db_connection = Database()  # init db connection
app = Flask(__name__)  # create flask app
api = Api(app)  # create api for flask app

parser = reqparse.RequestParser()  # init request parser
# arguments to parse for POST product
parser.add_argument('name', type=str, help='product name')
parser.add_argument('price_threshold', type=float, help='price threshold for notification')
parser.add_argument('url', type=str, help='product url')


# class for list of all products
class ProductList(Resource):
    @staticmethod
    def get() -> list:
        raw_result = db_connection.execute_query('SELECT name, price_threshold, url FROM products;')
        result_list = []
        for product in raw_result:
            product_dict = {
                'name': product[0],
                'price_threshold': product[1],
                'url': product[2]
            }
            result_list.append(product_dict)
        result = result_list
        return result


# class to add a new product
class CreateProduct(Resource):
    @staticmethod
    def post() -> str:
        arguments = parser.parse_args()  # parse arguments
        # get single arguments out of dict
        name = arguments['name']
        price_threshold = arguments['price_threshold']
        url = arguments['url']
        Database.insert_product(db_connection, name, price_threshold, url)
        return f'Inserted: name: {name} |price_threshold: {price_threshold} |url: {url}'


# class to fetch and delete product (future: edit)
class Product(Resource):
    @staticmethod
    def get(product_id: int) -> list:
        result = db_connection.execute_query(f'SELECT id, name, price_threshold, url FROM products WHERE id = {product_id}')
        return result

    @staticmethod
    def delete(product_id: int) -> str:
        Database.delete_product(db_connection, product_id)
        return f'Product with id {product_id} deleted'


# class to get price
class Price(Resource):
    @staticmethod
    def get(product_id: int) -> dict:
        raw_result = db_connection.execute_query(f'SELECT product_id, price FROM prices WHERE product_id = {product_id}')
        result = {'price': raw_result}
        return result


# create api routes
api.add_resource(ProductList, '/productlist')  # add productlist endpoint
api.add_resource(CreateProduct, '/product/create')  # add create endpoint
api.add_resource(Product, '/product/<product_id>')  # add product endpoint
api.add_resource(Price, '/price/<product_id>')  # add price endpoint

# main loop to run api
if __name__ == '__main__':
    app.run()

