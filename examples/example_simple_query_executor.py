import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.DatabaseConnector import DatabaseConnector
from src.SimpleQueryExecutor import SimpleQueryExecutor

# database parameters 
DATABASE_PARAMS = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "pwd",
    "database": "mydatabase" # create a database named "mydatabase" before running this script
}

# create a database connection
db_conn = DatabaseConnector(DATABASE_PARAMS)

# create an instance of the SimpleQueryExecutor class
query_executor = SimpleQueryExecutor(db_conn)

# create a new table with two columns (id and name)
query_executor.create_table('users', {'id': 'SERIAL PRIMARY KEY', 'name': 'VARCHAR(255)', 'age': 'INT'})

# insert some data into the table
query_executor.insert_data('users', {'name': 'John', 'age': 25})
query_executor.insert_data('users', {'name': 'Mary', 'age': 30})
query_executor.insert_data('users', {'name': 'Bob', 'age': 35})

# Select only the name and age columns for users aged 30 or older
results = query_executor.select_data('users', columns=['name', 'age'], where='age >= 30')

# print the results
print("name\t|age")
print("---------------")
for row in results:
    print("{}\t|{}".format(row[0], row[1]))

# drop the table
query_executor.drop_table('users')