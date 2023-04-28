from src.NativeQueryExecutor import NativeQueryExecutor
from src.DatabaseConnector import DatabaseConnector


class SimpleQueryExecutor(NativeQueryExecutor):
    """
    This class is responsible for executing SQL queries.
    It extends the NativeQueryExecutor class to execute simple SQL queries.
    """
    
    def __init__(self, db_conn: DatabaseConnector) -> None:
        """
        Constructor that stores the DatabaseConnector instance.
        """
        super().__init__(db_conn)


    def create_table(self, table_name: str, columns: dict) -> None:
        """
        Create a new table in the database.

        Parameters:
        ----------
        - table_name: The name of the table to create.
        - columns: A dictionary containing the names and data types of the columns.
        """
        sql = f"CREATE TABLE {table_name} ({','.join([f'{col_name} {data_type}' for col_name, data_type in columns.items()])})"
        self.execute_and_commit(sql)


    def select_data(self, table_name: str, columns: list = None, where_clause: str = None) -> list:
        """
        Select data from a table in the database.

        Parameters:
        ----------
        - table_name: The name of the table to select from.
        - columns: A list of column names to select.
        - where_clause: A WHERE clause to filter the results.

        Returns:
        -------
        returns a list of tuples containing the selected data.
        """
        col_names = '*' if columns is None else ','.join(columns)
        sql = f"SELECT {col_names} FROM {table_name}"
        
        if where_clause is not None:
            sql += f" WHERE {where_clause}"
        
        return self.execute_and_fetchall(sql)
    
    
    def insert_data(self, table_name: str, data: dict) -> None:
        """
        Insert data into a table in the database.

        Parameters:
        ----------
        - table_name: The name of the table to insert into.
        - data: A dictionary containing the column names and values to insert.
        """
        sql = f"INSERT INTO {table_name} ({','.join(data.keys())}) VALUES ({','.join(['%s' for _ in range(len(data))])})"
        self.execute_and_commit(sql, tuple(data.values()))
        

    def drop_table(self, table_name: str) -> None:
        """
        Drop a table from the database.

        Parameters:
        ----------
        - table_name: The name of the table to drop.
        """
        sql = f"DROP TABLE IF EXISTS {table_name}"
        self.execute_and_commit(sql)
