import mysql.connector as mysql  # import mysql connector for database connection
from Config import host, user, password, database  # import credentials from config file


# database class
class Database(object):
    def __init__(self):  # init function to create connection
        # enable connection with data from .env file
        self.db_connection = mysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        # set db cursor with buffered parameter
        self.db_cursor = self.db_connection.cursor(buffered=True)

    def execute_migration(self, migrations):
        self.db_cursor.execute('CREATE TABLE IF NOT EXISTS migrations '
                               '(id INT AUTO_INCREMENT PRIMARY KEY, '
                               'name VARCHAR(255), '
                               'executed BOOLEAN DEFAULT FALSE);')
        for migration in migrations:
            executed_migrations_raw = self.execute_query('SELECT name FROM migrations WHERE executed = 1;')
            executed_migrations = []
            for executed_migration in executed_migrations_raw:
                executed_migrations.append(executed_migration[0])
            if migration not in executed_migrations:
                self.db_cursor.execute('INSERT INTO migrations (name) VALUES (%s);', (migration,))
                self.db_cursor.execute(migrations[migration])
                self.db_connection.commit()
                self.db_cursor.execute('UPDATE migrations '
                                       'SET executed = 1'
                                       'WHERE name = (%s);', (migration,))
                self.db_connection.commit()
            else:
                pass
