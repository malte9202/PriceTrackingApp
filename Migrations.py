from Database import Database  # import database class


# function to execute the migrations that were not executed so far
def migrate() -> None:
    migrations = {
        'migration_0001': 'CREATE TABLE IF NOT EXISTS products '
                          '(id INT AUTO_INCREMENT PRIMARY KEY, '
                          'name VARCHAR(255),'
                          'price_threshold FLOAT, '
                          'url VARCHAR(255));',
        'migration_0002': 'CREATE TABLE IF NOT EXISTS prices '
                          '(product_id INT NOT NULL, '
                          'price FLOAT NOT NULL, '
                          'scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);'
    }
    database = Database()
    Database.execute_migration(database, migrations)
