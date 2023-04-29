from psycopg2_wrapper.DatabaseConnector import DatabaseConnector

class NativeQueryExecutor:
    """
    This class is responsible for executing SQL queries. 
    It takes an instance of DatabaseConnector to establish a database connection.
    """

    def __init__(self, config: dict) -> None:
        """
        Constructor that takes an instance of DatabaseConnector to establish a database connection.

        Parameters:
        db_conn (DatabaseConnector): An instance of DatabaseConnector.
        """
        self.conn = DatabaseConnector(db_params=config)


    def execute(self, sql: str, params: tuple = None) -> tuple:
        """
        Execute a SQL query.
        
        Parameters:
        ----------
        - sql: The SQL query to execute.
        - params: The parameters to pass to the query.
        
        Returns:
        -------
        returns a cursor object and a connection object.
        """
        conn = self.conn.connect()
        cursor = conn.cursor()

        if params is None: cursor.execute(sql)
        else: cursor.execute(sql, params)

        return cursor, conn


    def execute_and_commit(self, sql: str, params: tuple = None) -> None:
        """
        Execute a SQL query and commit the changes to the database.
        
        Parameters:
        ----------
        - sql: The SQL query to execute.
        - params: The parameters to pass to the query.
        """
        cursor, conn = self.execute(sql, params)
        conn.commit()  
        self.conn.close(cursor, conn)
        
        
    def execute_and_fetchone(self, sql: str, params: tuple = None) -> tuple:
        """
        Execute a SQL query and fetch the first result.
        
        Parameters:
        ----------
        - sql: The SQL query to execute.
        - params: The parameters to pass to the query.
        
        Returns:
        -------
        returns a tuple with the result.
        """
        cursor, conn = self.execute(sql, params)
        result = cursor.fetchone()

        self.conn.close(cursor, conn)        
        return result
    
    
    def execute_and_fetchall(self, sql: str, params: tuple = None) -> list:
        """
        Execute a SQL query and fetch all the results.
        
        Parameters:
        ----------
        - sql: The SQL query to execute.
        - params: The parameters to pass to the query.
        
        Returns:
        -------
        returns a list with the results.
        """
        cursor, conn = self.execute(sql, params)
        result = cursor.fetchall()
        
        self.conn.close(cursor, conn)
        return result
    
    
    def execute_and_fetchmany(self, sql: str, params: tuple = None, size: int = 2) -> list:
        """
        Execute a SQL query and fetch a number of results.
        
        Parameters:
        ----------
        - sql: The SQL query to execute.
        - params: The parameters to pass to the query.
        - size: The number of results to fetch.
        
        Returns:
        -------
        returns a list with the results.
        """
        cursor, conn = self.execute(sql, params)
        result = cursor.fetchmany(size)

        self.conn.close(cursor, conn)
        return result
    
    
    def execute_many_and_commit(self, sql: str, params: list) -> None:
        """
        Execute a SQL query with multiple parameters.
        
        Parameters:
        ----------
        - sql: The SQL query to execute.
        - params: A list of parameters to pass to the query.
        """
        conn = self.conn.connect()
        cursor = conn.cursor()
        
        cursor.executemany(sql, params)
        conn.commit()
        
        self.conn.close(cursor, conn)