import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


from psycopg2_wrapper.NativeQueryExecutor import NativeQueryExecutor

# database parameters 
DATABASE_PARAMS = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "pwd",
    "database": "mydatabase" # create a database named "mydatabase" before running this script
}


# create a NativeQueryExecutor instance
query_executor = NativeQueryExecutor(config=DATABASE_PARAMS)

# create a table in the database
create_table_query = """
					CREATE TABLE example_table (
						id INT PRIMARY KEY,
						name VARCHAR(50),
						age INT
					)
					"""
query_executor.execute_and_commit(create_table_query)


# insert some data
insert_data_query = """
                    INSERT INTO example_table (id, name, age)
                    VALUES (%s, %s, %s)
                    """
    
# each row is a tuple of values to be inserted
params = [
    (1, 'Alice', 25),
    (2, 'Bob', 30),
    (3, 'Charlie', 35)
]
query_executor.execute_many_and_commit(insert_data_query, params)

# query the table
query_data_query = "SELECT * FROM example_table"
result = query_executor.execute_and_fetchall(query_data_query)

# print the result 
print("id\t|name\t|age")
print("------------------")
for row in result:
	print("{}\t|{}\t|{}".format(row[0], row[1], row[2]))

 
# delete the table
drop_table_query = "DROP TABLE example_table"
query_executor.execute_and_commit(drop_table_query)