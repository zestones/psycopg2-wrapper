import configparser
import os

# Path to the database configuration file
DB_CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), './', 'config.ini'))

# Read the database configuration file
config = configparser.ConfigParser()
config.read(DB_CONFIG_PATH)

DATABASE_PARAMS = {
    'host': config.get('postgresql.db', 'database.host'),
    'user': config.get('postgresql.db', 'database.user'),
    'password': config.get('postgresql.db', 'database.password'),
    'port': config.get('postgresql.db', 'database.port'),
    'database': config.get('postgresql.db', 'database.name')
}