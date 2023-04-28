from src.DatabaseConnector import DatabaseConnector
from src.SimpleQueryExecutor import SimpleQueryExecutor

import pytest


@pytest.fixture
def db_conn():
    params = {"database": "test_db", "user": "postgres", "password": "pwd", "host": "localhost"}
    return DatabaseConnector(db_params=params)


def test_create_table(db_conn):
    sqe = SimpleQueryExecutor(db_conn)
    sqe.create_table(
        "test_table", {"id": "SERIAL PRIMARY KEY", "name": "VARCHAR(50)", "age": "INTEGER"})
    cursor, conn = sqe.execute_and_fetchall(
        "SELECT * FROM information_schema.tables WHERE table_name='test_table';")
    result = cursor.fetchall()
    assert len(result) == 1
    assert result[0][2] == "test_table"
    sqe.execute_and_commit("DROP TABLE test_table;")



def test_insert_data(db_conn):
    sqe = SimpleQueryExecutor(db_conn)
    sqe.create_table(
        "test_table", {"id": "SERIAL PRIMARY KEY", "name": "VARCHAR(50)", "age": "INTEGER"})
    sqe.insert_data("test_table", ["name", "age"], [
                    ("John", 35), ("Jane", 25)])
    cursor, conn = sqe.execute_and_fetchall(
        "SELECT * FROM test_table ORDER BY id;")
    result = cursor.fetchall()
    assert len(result) == 2
    assert result[0][1] == "John"
    assert result[0][2] == 35
    assert result[1][1] == "Jane"
    assert result[1][2] == 25
    sqe.execute_and_commit("DROP TABLE test_table;")


def test_select_data(db_conn):
    sqe = SimpleQueryExecutor(db_conn)
    sqe.create_table(
        "test_table", [{"id": "SERIAL PRIMARY KEY", "name": "VARCHAR(50)", "age": "INTEGER"}])
    sqe.insert_data("test_table", ["name", "age"], [
                    ("John", 35), ("Jane", 25)])
    result = sqe.select_data("test_table", ["name", "age"], "age > 30")
    assert len(result) == 1
    assert result[0][0] == "John"
    assert result[0][1] == 35
    sqe.execute_and_commit("DROP TABLE test_table;")


def test_alter_table(db_conn):
    sqe = SimpleQueryExecutor(db_conn)
    sqe.create_table(
        "test_table", [{"id": "SERIAL PRIMARY KEY", "name": "VARCHAR(50)", "age": "INTEGER"}])
    sqe.alter_table("test_table", "ADD COLUMN gender CHAR(1)")
    cursor, conn = sqe.execute_and_fetchall(
        "SELECT column_name FROM information_schema.columns WHERE table_name='test_table' ORDER BY column_name;")
    result = cursor.fetchall()
    assert len(result) == 4
    assert result[0][0] == "age"
    assert result[1][0] == "gender"
    assert result[2][0] == "id"
    assert result[3][0] == "name"
    sqe.execute_and_commit("DROP TABLE test_table;")


def test_drop_table(db_conn):
    sqe = SimpleQueryExecutor(db_conn)
    sqe.create_table(
        "test_table", [{"id": "SERIAL PRIMARY KEY", "name": "VARCHAR(50)", "age": "INTEGER"}])
    sqe.drop_table("test_table")
    cursor, conn = sqe.execute_and_fetchall(
        "SELECT * FROM information_schema.tables WHERE table_name='test_table';")
    result = cursor.fetchall()
    assert len(result) == 0
