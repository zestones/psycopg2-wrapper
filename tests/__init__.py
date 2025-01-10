import configparser
import os

# Path to the database configuration file
# DB_CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), './', 'config.ini'))

# # Read the database configuration file
# config = configparser.ConfigParser()
# config.read(DB_CONFIG_PATH)

DATABASE_PARAMS = {
    'host': 'localhost',
    'user': 'postgres',
    'password': '1234',
    'port': '5432',
    'database': 'test'
}