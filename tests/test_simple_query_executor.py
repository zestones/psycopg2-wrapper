# test_simple_query_executor.py

import pytest
from psycopg2_wrapper.SimpleQueryExecutor import SimpleQueryExecutor

from . import DATABASE_PARAMS


@pytest.fixture
def db_params():
    """
    Fixture to provide database parameters for tests.
    Returns:
        dict: A dictionary containing the database connection parameters.
    """
    return DATABASE_PARAMS

@pytest.fixture
def simple_query_executor(db_params):
    """
    Fixture to create an instance of SimpleQueryExecutor for testing.
    
    Args:
        db_params (dict): Database connection parameters.

    Returns:
        SimpleQueryExecutor: An instance of the query executor for simple operations.
    """
    return SimpleQueryExecutor(db_params)

def test_create_table(simple_query_executor):
    """
    Test creating a table.
    Ensures that the `create_table` method creates a table with the specified schema.

    Args:
        simple_query_executor (SimpleQueryExecutor): Fixture for executing simple queries.
    """
    simple_query_executor.create_table('test_table', {'id': 'SERIAL PRIMARY KEY', 'name': 'VARCHAR(100)'})

    result = simple_query_executor.execute_and_fetchone("SELECT to_regclass('public.test_table')")
    assert result[0] == 'test_table'

    simple_query_executor.drop_table('test_table')

def test_insert_data(simple_query_executor):
    """
    Test inserting data into a table.
    Ensures that the `insert_data` method correctly inserts rows into the specified table.

    Args:
        simple_query_executor (SimpleQueryExecutor): Fixture for executing simple queries.
    """
    simple_query_executor.create_table('test_table', {'id': 'SERIAL PRIMARY KEY', 'name': 'VARCHAR(100)'})
    simple_query_executor.insert_data('test_table', {'name': 'Test'})
    
    result = simple_query_executor.select_data('test_table', ['name'])
    assert result == [('Test',)]
    
    simple_query_executor.drop_table('test_table')

def test_select_data(simple_query_executor):
    """
    Test selecting data from a table.
    Ensures that the `select_data` method retrieves the expected rows from the table.

    Args:
        simple_query_executor (SimpleQueryExecutor): Fixture for executing simple queries.
    """
    simple_query_executor.create_table('test_table', {'id': 'SERIAL PRIMARY KEY', 'name': 'VARCHAR(100)'})
    simple_query_executor.insert_data('test_table', {'name': 'Test'})
    
    result = simple_query_executor.select_data('test_table', ['name'])
    assert result == [('Test',)]
    
    simple_query_executor.drop_table('test_table')

def test_drop_table(simple_query_executor):
    """
    Test dropping a table.
    Ensures that the `drop_table` method removes the table from the database.

    Args:
        simple_query_executor (SimpleQueryExecutor): Fixture for executing simple queries.
    """
    simple_query_executor.create_table('test_table', {'id': 'SERIAL PRIMARY KEY', 'name': 'VARCHAR(100)'})
    simple_query_executor.drop_table('test_table')
    
    result = simple_query_executor.execute_and_fetchone("SELECT to_regclass('public.test_table')")
    assert result[0] is None