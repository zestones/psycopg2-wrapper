import psycopg2


class DatabaseConnector:
    """
    This class is a wrapper around the psycopg2 library to simplify the connection and execution of SQL queries.
    The class is designed to be inherited by all DAO classes in the project.
    """

    def __init__(self, db_params: dict) -> None:
        """
        Constructor that stores the database parameters to establish a connection.

        Parameters:
        ----------
        db_params (dict): A dictionary containing the database parameters.
            The dict is retrieved from the config.ini file.

        Format:
        -------
        {
            "database": "database_name",
            "user": "username",
            "password": "password",
            "host": "host",
            "port": "port"
        }
        """
        # check if a key is missing and set it to None
        keys = ["database", "user", "password", "host", "port"]                
        self.db_params = {key: db_params.get(key, None) for key in keys}

    def connect(self) -> psycopg2.extensions.connection:
        """
        Create a connection to the database.

        Returns:
        -------
        returns a connection object.
        """
        conn = psycopg2.connect(
            host=self.db_params["host"],
            database=self.db_params['database'],
            user=self.db_params["user"],
            password=self.db_params["password"],
            port=self.db_params["port"]
        )

        return conn

    def close(self, cursor: psycopg2.extensions.cursor, conn: psycopg2.extensions.connection) -> None:
        """
        Close the cursor and connection objects.

        Parameters:
        ----------
        - cursor: The cursor object to close.
        - conn: The connection object to close.
        """
        cursor.close()
        conn.close()
