import pytest
import psycopg2

from src.SimpleQueryExecutor import SimpleQueryExecutor
from src.DatabaseConnector import DatabaseConnector

from . import DATABASE_PARAMS


@pytest.fixture(scope="module")
def db_conn():
    # Setup
    conn = psycopg2.connect(
        host=DATABASE_PARAMS["host"],
        user=DATABASE_PARAMS["user"],
        password=DATABASE_PARAMS["password"]
    )
    conn.set_isolation_level(0)
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE {DATABASE_PARAMS['database']}")
    cur.close()

    db_conn = DatabaseConnector(db_params=DATABASE_PARAMS)
    query_executor = SimpleQueryExecutor(db_conn)
    query_executor.create_table("test_table", {"id": "INTEGER PRIMARY KEY", "name": "TEXT"})
    yield db_conn

    # Teardown
    query_executor.drop_table("test_table")


@pytest.fixture(scope="module")
def query_executor(db_conn):
    query_executor = SimpleQueryExecutor(db_conn)
    yield query_executor


def test_create_table(query_executor):
    query_executor.create_table("test_table_2", {"id": "INTEGER PRIMARY KEY", "name": "TEXT"})
    assert len(query_executor.select_data("test_table_2")) == 0


def test_select_data(query_executor):
    data = {"id": 1, "name": "John"}
    query_executor.insert_data("test_table", data)
    assert query_executor.select_data("test_table", where_clause="id=1") == [(1, "John")]


def test_insert_data(query_executor):
    data = {"id": 2, "name": "Jane"}
    query_executor.insert_data("test_table", data)
    assert query_executor.select_data("test_table", where_clause="id=2") == [(2, "Jane")]


def test_drop_table(query_executor):
    query_executor.create_table("test_table_3", {"id": "INTEGER PRIMARY KEY", "name": "TEXT"})
    query_executor.drop_table("test_table_3")
    with pytest.raises(Exception):
        query_executor.select_data("test_table_3")