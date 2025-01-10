# test_native_query_executor.py

from psycopg2 import ProgrammingError
from psycopg2_wrapper.NativeQueryExecutor import NativeQueryExecutor
import pytest

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
def native_query_executor(db_params):
    """
    Fixture to create an instance of NativeQueryExecutor for testing.
    
    Args:
        db_params (dict): Database connection parameters.

    Returns:
        NativeQueryExecutor: An instance of the query executor for interacting with the database.
    """
    return NativeQueryExecutor(db_params)

def test_execute(native_query_executor):
    """
    Test executing a simple SQL query.
    Ensures that the `execute` method works and fetches the expected result.

    Args:
        native_query_executor (NativeQueryExecutor): Fixture for executing queries.
    """
    cursor, _ = native_query_executor.execute("SELECT 1")
    result = cursor.fetchone()
    assert result == (1,)

def test_execute_invalid_sql(native_query_executor):
    """
    Test executing an invalid SQL query.
    Ensures that the `execute` method raises a `ProgrammingError` for invalid SQL.

    Args:
        native_query_executor (NativeQueryExecutor): Fixture for executing queries.
    """
    with pytest.raises(ProgrammingError):
        native_query_executor.execute("SELCT 1")

def test_execute_and_commit(native_query_executor):
    """
    Test executing and committing a SQL statement.
    Ensures that the `execute_and_commit` method creates and drops a table correctly.

    Args:
        native_query_executor (NativeQueryExecutor): Fixture for executing queries.
    """
    sql = "CREATE TABLE IF NOT EXISTS test_table (id SERIAL PRIMARY KEY)"
    native_query_executor.execute_and_commit(sql)
    
    result = native_query_executor.execute_and_fetchone("SELECT to_regclass('public.test_table')")
    assert result[0] == 'test_table'
    
    native_query_executor.execute_and_commit("DROP TABLE IF EXISTS test_table")

def test_execute_and_fetchone(native_query_executor):
    """
    Test executing a query and fetching a single result.
    Ensures that the `execute_and_fetchone` method returns the expected result.

    Args:
        native_query_executor (NativeQueryExecutor): Fixture for executing queries.
    """
    result = native_query_executor.execute_and_fetchone("SELECT 1")
    assert result == (1,)

def test_execute_and_fetchall(native_query_executor):
    """
    Test executing a query and fetching all results.
    Ensures that the `execute_and_fetchall` method returns all rows.

    Args:
        native_query_executor (NativeQueryExecutor): Fixture for executing queries.
    """
    result = native_query_executor.execute_and_fetchall("SELECT 1 UNION SELECT 2")
    assert result == [(1,), (2,)]

def test_execute_and_fetchmany(native_query_executor):
    """
    Test executing a query and fetching a limited number of results.
    Ensures that the `execute_and_fetchmany` method returns the specified number of rows.

    Args:
        native_query_executor (NativeQueryExecutor): Fixture for executing queries.
    """
    result = native_query_executor.execute_and_fetchmany("SELECT 1 UNION SELECT 2 UNION SELECT 3", size=2)
    assert result == [(1,), (2,)]

def test_execute_many_and_commit(native_query_executor):
    """
    Test executing multiple SQL statements and committing them.
    Ensures that the `execute_many_and_commit` method correctly inserts multiple rows into a table.

    Args:
        native_query_executor (NativeQueryExecutor): Fixture for executing queries.
    """
    sql = "INSERT INTO test_table (id) VALUES (%s)"
    params = [(1,), (2,), (3,)]
    
    native_query_executor.execute_and_commit("CREATE TABLE IF NOT EXISTS test_table (id INT)")
    native_query_executor.execute_many_and_commit(sql, params)
    
    result = native_query_executor.execute_and_fetchall("SELECT * FROM test_table")
    assert result == [(1,), (2,), (3,)]
    
    native_query_executor.execute_and_commit("DROP TABLE IF EXISTS test_table")