# Psycopg2-Wrapper
[![Upload Python Package](https://github.com/zestones/psycopg2-wrapper/actions/workflows/PyPi-deploy.yml/badge.svg)](https://github.com/zestones/psycopg2-wrapper/actions/workflows/PyPi-deploy.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Realease](https://img.shields.io/github/v/release/zestones/psycopg2-wrapper)](https://img.shields.io/github/v/release/zestones/psycopg2-wrapper)

Psycopg2-Wrapper is a Python library that provides a simple and easy-to-use interface for executing SQL queries using Psycopg2. It is designed to make it easy for developers to interact with PostgreSQL databases from Python applications.


## Features

- Simple and easy-to-use interface for executing SQL queries using Psycopg2.
- Supports all standard SQL statements, including SELECT, INSERT, UPDATE, and DELETE.
- Provides methods for executing single and multiple queries, fetching results, and committing changes to the database.
- Built-in support for connection pooling.
- Lightweight and easy to install, with no external dependencies.

## Installation

To install Psycopg2-Wrapper, you can use pip:

```
pip install psycopg2-wrapper
```

## Usage

To use Psycopg2-Wrapper in your Python application, you first need to import one of the query executor classes from the `psycopg2_wrapper` module:

```python
from psycopg2_wrapper.SimpleQueryExecutor import SimpleQueryExecutor
# or
from psycopg2_wrapper.NativeQueryExecutor import NativeQueryExecutor
```
<details>
<summary style="font-weight: bold; font-size: 1.2em;">Configuration</summary>

Before you can execute SQL queries using Psycopg2-Wrapper, you need to configure the connection to the PostgreSQL server. You can do this by creating a configuration dictionary with the following fields:

```python
config = {
    "host": "localhost",
    "port": "5432", # if not specified, default port 5432 will be used
    "database": "mydatabase",
    "user": "myusername",
    "password": "mypassword"
}
```

- `host`: The hostname of the PostgreSQL server.
- `port`: The port number of the PostgreSQL server.
- `database`: The name of the PostgreSQL database to connect to.
- `user`: The username to use for authentication.
- `password`: The password to use for authentication.

Check out the [Psycopg2 documentation](https://www.psycopg.org/docs/module.html) for more information about the configuration options.
</details>

---

<details>
<summary style="font-weight: bold; font-size: 1.2em;"> NativeQueryExecutor </summary>

The `NativeQueryExecutor` class allows you to execute native SQL queries using Psycopg2. You can create an instance of the class and use its `execute_query` method to execute SQL queries:

```python
# create a NativeQueryExecutor instance
query_executor = NativeQueryExecutor(config)
```	

The `NativeQueryExecutor` class takes a configuration dictionary as described [here](#configuration).

This class implements the following methods for executing SQL queries:

Query to read data from the database:
```python
def execute_and_fetchone(self, sql: str, params: tuple = None) -> tuple:
def execute_and_fetchmany(self, sql: str, params: tuple = None, size: int = 2) -> list:
def execute_and_fetchall(self, sql: str, params: tuple = None) -> list:
```

And query to write/modify data to the database:

```python
def execute_and_commit(self, sql: str, params: tuple = None) -> None:
def execute_many_and_commit(self, sql: str, params: list) -> None:
```

<details>
<summary style="font-weight: bold; font-size: 1em;">Read data from the database</summary>

### Execute and fetchone

```python
# the sql query
query_data_query = "SELECT * FROM example_table WHERE id = %s"
# the parameters of the query
param = (1,)
# execute the query and fetch the results
result = query_executor.execute_and_fetchone(query_data_query, param)
```
The `execute_and_fetchone` method takes two parameters: the **SQL query** to execute, and **an optional tuple of parameters** to pass to the query.
The method returns a tuple containing the results of the query.

### Execute and fetchmany
```python
# the sql query
query_data_query = "SELECT * FROM example_table WHERE id = %s"
# the parameters of the query
param = (1,)
# execute the query and fetch the results
result = query_executor.execute_and_fetchmany(query_data_query, param, 4)
```
The `execute_and_fetchmany` method takes three parameters: the **SQL query** to execute, **an optional tuple of parameters** to pass to the query, and **an optional size** parameter that specifies the maximum number of rows to fetch.


### Execute and fetchall
```python
# the sql query
query_data_query = "SELECT * FROM example_table WHERE id = %s"
# the parameters of the query
param = (1,)
# execute the query and fetch the results
result = query_executor.execute_and_fetchall(query_data_query)
```
The `execute_and_fetchall` method takes two parameters: the **SQL query** to execute, and **an optional tuple of parameters** to pass to the query.

---

</details>



<details>
<summary style="font-weight: bold; font-size: 1em;">Write/modify data to the database</summary>

### Execute and commit
````python
# the sql query
query_data_query = "INSERT INTO example_table (id, name) VALUES (%s, %s)"
# the parameters of the query
param = (1, 'John')
# execute the query and commit the changes
query_executor.execute_and_commit(query_data_query, param)
````
The `execute_and_commit` method takes two parameters: the **SQL query** to execute, and **an optional tuple of parameters** to pass to the query.

### Execute many and commit
````python
# the sql query
query_data_query = "INSERT INTO example_table (id, name) VALUES (%s, %s)"
# the parameters of the query
params = [(1, 'John'), (2, 'Jane'), (3, 'Jack')]
# execute the query and commit the changes
query_executor.execute_many_and_commit(query_data_query, params)
````
The `execute_many_and_commit` method takes two parameters: the **SQL query** to execute, and **a list of tuples of parameters** to pass to the query.

Check out the [NativeQueryExecutor example](./examples/example_native_query_executor.py) for more examples of how to use the `NativeQueryExecutor` class.
</details>
</details>

---

<details>
<summary style="font-weight: bold; font-size: 1.2em;">SimpleQueryExecutor</summary>

The `SimpleQueryExecutor` class extends the `NativeQueryExecutor` class and provides methods for executing simple SQL queries. Here are some usage examples:

First we start by instantiating the `SimpleQueryExecutor` class:
```python
# Define database configuration
config = {
    'host': 'localhost',
    'port': 5432,
    'database': 'my_database',
    'user': 'my_user',
    'password': 'my_password'
}
# Create an instance of SimpleQueryExecutor
query_executor = SimpleQueryExecutor(config)
```

The `SimpleQueryExecutor` class takes a configuration dictionary as described [here](#configuration).

### Creating a table
```python

# Define the columns for the new table
columns = {
    'id': 'SERIAL PRIMARY KEY',
    'name': 'VARCHAR(255)',
    'age': 'INTEGER'
}

# Create the new table
query_executor.create_table('my_table', columns)
```

The `create_table` method takes two parameters: the name of the table to create, and a dictionary of column names and their data types.

### Selecting data from a table

```python
# Select all columns from the 'my_table' table
results = query_executor.select_data('my_table')
print(results)

# Select only the 'name' and 'age' columns from the 'my_table' table
results = query_executor.select_data('my_table', columns=['name', 'age'])
print(results)

# Select only the 'name' column from the 'my_table' table where age is greater than or equal to 18
results = query_executor.select_data('my_table', columns=['name'], where='age >= 18')
print(results)
```
The `select_data` method takes three parameters: the **name of the table** to select data from, a **list of column names to select**, and **an optional `where_clause` parameter** to filter the results.


### Inserting data into a table

```python
# Define the data to insert
data = {
    'name': 'John',
    'age': 25
}

# Insert the data into the 'my_table' table
query_executor.insert_data('my_table', data)
```
The `insert_data` method takes two parameters: **the name of the table** to insert data into, and **a dictionary of column names and their corresponding values**.


### Dropping a table

```python
# Drop the 'my_table' table
query_executor.drop_table('my_table')
```
The `drop_table` method takes one parameter: **the name of the table** to drop.

For more examples of how to use the `SimpleQueryExecutor` class, check out the [SimpleQueryExecutor example](./examples/example_simple_query_executor.py).
</details>