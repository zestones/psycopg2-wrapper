from psycopg2_wrapper.NativeQueryExecutor import NativeQueryExecutor
from psycopg2_wrapper.DatabaseConnector import DatabaseConnector

import pytest
import psycopg2

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
def query_execution(db_params):
    # create a NativeQueryExecutor instance for the test database
    return NativeQueryExecutor(db_params)


def test_execute_and_commit(query_execution):

    sql = "CREATE TABLE test_table (id SERIAL PRIMARY KEY, name TEXT)"
    query_execution.execute_and_commit(sql)

    sql = "INSERT INTO test_table (name) VALUES (%s)"
    params = ("test_name",)
    query_execution.execute_and_commit(sql, params)

    sql = "SELECT name FROM test_table WHERE id=1"
    result = query_execution.execute_and_fetchone(sql)
    assert result == ("test_name",)


def test_execute_and_fetchone(query_execution):
    
    sql = "SELECT name FROM test_table WHERE id=1"
    result = query_execution.execute_and_fetchone(sql)
    
    assert result == ("test_name",)


def test_execute_and_fetchall(query_execution):
    
    sql = "SELECT name FROM test_table"
    result = query_execution.execute_and_fetchall(sql)
    
    assert result == [("test_name",)]


def test_execute_and_fetchmany(query_execution):
    # test the execute_and_fetchmany method
    sql = "SELECT name FROM test_table"
    result = query_execution.execute_and_fetchmany(sql, size=1)
    assert result == [("test_name",)]


def test_execute_many_and_commit(query_execution):

    # test the execute_many_and_commit method
    sql = "INSERT INTO test_table (name) VALUES (%s)"
    params = [("test_name_2",), ("test_name_3",)]
    query_execution.execute_many_and_commit(sql, params)

    sql = "SELECT name FROM test_table ORDER BY id"
    result = query_execution.execute_and_fetchall(sql)
    assert result == [("test_name",), ("test_name_2",), ("test_name_3",)]


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