from Database import Database
from Scraper import Scraper
from Migrations import migrate

migrate()  # runs all migrations, only new migrations are executed

database = Database()  # create db connection

product_ids = Database.get_product_ids(database)  # fetch all product_ids from database

for product_id in product_ids:
    url = Database.get_url(database, product_id)
    price = Scraper.scrape_price(url)
    Database.insert_price(database, product_id, price)
