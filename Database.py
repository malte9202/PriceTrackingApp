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
