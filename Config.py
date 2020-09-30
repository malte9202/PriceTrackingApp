import os  # import operating system functions
from dotenv import load_dotenv, find_dotenv  # import dotenv module to access .env file

load_dotenv(find_dotenv())  # find .env file and load it

user = os.environ.get('USERNAME')  # get username from .env
password = os.environ.get('PASSWORD')  # get password from .env
host = os.environ.get('HOST')  # get host from .env
database = os.environ.get('DATABASE')  # get database from .env
