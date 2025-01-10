# test_database_connector.py

from psycopg2_wrapper.DatabaseConnector import DatabaseConnector
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

def test_database_connector_init(db_params):
    """
    Test the initialization of the DatabaseConnector class.
    Ensures that the provided database parameters are correctly stored.

    Args:
        db_params (dict): Database parameters fixture.
    """
    db_conn = DatabaseConnector(db_params)
    assert db_conn.db_params == db_params

def test_database_connector_connect(db_params):
    """
    Test successful database connection.
    Ensures that the `connect` method returns a valid connection object.

    Args:
        db_params (dict): Database parameters fixture.
    """
    db_conn = DatabaseConnector(db_params)
    conn = db_conn.connect()
    
    assert conn is not None

def test_database_connector_connect_invalid():
    """
    Test database connection failure with invalid parameters.
    Ensures that the `connect` method raises an `Exception`
    when provided with incorrect credentials.
    """
    invalid_params = {
        "host": "localhost",
        "user": "invalid_user",
        "password": "wrong_pass",
        "port": "5432",
        "database": "test",
    }
    db_conn = DatabaseConnector(invalid_params)
    with pytest.raises(Exception):
        db_conn.connect()

def test_database_connector_close(db_params):
    """
    Test closing the database connection and cursor.
    Ensures that both the connection and cursor are properly closed.

    Args:
        db_params (dict): Database parameters fixture.
    """
    db_conn = DatabaseConnector(db_params)
    
    conn = db_conn.connect()
    cursor = conn.cursor()
    
    db_conn.close(cursor, conn)
    assert conn.closed == 1
