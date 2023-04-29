import pytest
import psycopg2

from psycopg2_wrapper.SimpleQueryExecutor import SimpleQueryExecutor
from psycopg2_wrapper.DatabaseConnector import DatabaseConnector

from . import DATABASE_PARAMS


@pytest.fixture(scope="session")
def db_params():
    # create a test database and return the database parameters
    conn = psycopg2.connect(
        host=DATABASE_PARAMS["host"],
        user=DATABASE_PARAMS["user"],
        password=DATABASE_PARAMS["password"]
    )
    
    conn.set_isolation_level(0)
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE {DATABASE_PARAMS['database']}")
    conn.close()
    
    return DATABASE_PARAMS


@pytest.fixture(scope="function")
def query_executor(db_params):
    query_executor = SimpleQueryExecutor(config=db_params)
    yield query_executor


def test_create_table(query_executor):
    query_executor.create_table("test_table", {"id": "INTEGER PRIMARY KEY", "name": "TEXT"})
    assert len(query_executor.select_data("test_table")) == 0


def test_select_data(query_executor):
    data = {"id": 1, "name": "John"}
    query_executor.insert_data("test_table", data)
    assert query_executor.select_data("test_table", where="id=1") == [(1, "John")]


def test_insert_data(query_executor):
    data = {"id": 2, "name": "Jane"}
    query_executor.insert_data("test_table", data)
    assert query_executor.select_data("test_table", where="id=2") == [(2, "Jane")]


def test_drop_table(query_executor):
    query_executor.create_table("test_table_2", {"id": "INTEGER PRIMARY KEY", "name": "TEXT"})
    query_executor.drop_table("test_table_2")
    with pytest.raises(Exception):
        query_executor.select_data("test_table_2")
        

@pytest.fixture(scope="session", autouse=True)
def drop_test_db(request):
    # drop the test database after all tests are finished
    def finalizer():

        conn = psycopg2.connect(
            host=DATABASE_PARAMS["host"],
            user=DATABASE_PARAMS["user"],
            password=DATABASE_PARAMS["password"]
        )

        conn.set_isolation_level(0)
        cur = conn.cursor()
        cur.execute(f"DROP DATABASE IF EXISTS {DATABASE_PARAMS['database']}")
        conn.close()

    request.addfinalizer(finalizer)