import mysql.connector
import pandas as pd
from model.database.Database.AbstractDatabase import AbstractDatabase
from model.database.mysql_constants import HOST, DBNAME, USERNAME, PASSWORD


class Database(AbstractDatabase):
    @classmethod
    def connect_to_mysql(cls) -> None:
        try:
            cls._connection = mysql.connector.connect(
                host=HOST,
                database=DBNAME,
                user=USERNAME,
                password=PASSWORD
            )
        except Exception as e:
            print("Error connecting to MySQL:", e)
            cls._connection = None

    @classmethod
    def get_connection(cls) -> mysql.connector.connection.MySQLConnection:
        if cls._connection is None or not cls._connection.is_connected():
            cls.connect_to_mysql()
        return cls._connection

    @classmethod
    def close_connection(cls) -> None:
        try:
            if cls._connection is not None and cls._connection.is_connected():
                cls._connection.close()
        except Exception as e:
            print("Error closing connection:", e)
        finally:
            # Reset the connection attribute to None
            cls._connection = None

    @classmethod
    def read_mysql_to_dataframe(cls, query: str) -> pd.DataFrame:
        try:
            cursor = cls.get_connection().cursor()
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
            cursor.close()
            return pd.DataFrame(data, columns=columns)
        except Exception as e:
            print("Error executing MySQL query:", e)
            return pd.DataFrame()

    @classmethod
    def db_process(cls, query: str, fetchone: bool = True, commit_needed: bool = False, params: tuple | None = None):
        connection = cls.get_connection()
        cursor = connection.cursor()

        try:
            if params is None:
                cursor.execute(query)
            else:
                cursor.execute(query, params)

            data = None
            if commit_needed:
                connection.commit()
            elif fetchone:
                # Fetch one row
                data = cursor.fetchone()
                # Consume all remaining rows to avoid InternalError
                while cursor.fetchone():
                    continue
            else:
                # Fetch all rows
                data = cursor.fetchall()

        finally:
            # Ensure the cursor is closed even if an error occurs
            cursor.close()
            # Close the connection
            cls.close_connection()

        return data
