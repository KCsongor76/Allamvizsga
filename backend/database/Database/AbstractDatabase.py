from abc import ABC, abstractmethod
import mysql.connector
import pandas as pd


class AbstractDatabase(ABC):
    _connection: mysql.connector.connection.MySQLConnection | None = None

    @classmethod
    @abstractmethod
    def connect_to_mysql(cls) -> None:
        """
        Gives you access to the class' connection attribute.
        :return:
        """
        pass

    @classmethod
    @abstractmethod
    def get_connection(cls) -> mysql.connector.connection.MySQLConnection:
        """
        Getter function for the connection attribute.
        :return: mysql.connector.connection.MySQLConnection
        """
        pass

    @classmethod
    @abstractmethod
    def close_connection(cls) -> None:
        """
        Closes the connection attribute, and resets it to None.
        :return:
        """
        pass

    @classmethod
    @abstractmethod
    def read_mysql_to_dataframe(cls, query: str) -> pd.DataFrame:
        """
        Given the query parameter, executes an SQL query returning the data in a Dataframe.
        :param query:
        :return:
        """
        pass

    @classmethod
    @abstractmethod
    def db_process(cls, query: str, fetchone: bool, params: tuple, commit_needed: bool):
        """
        Open: connection, cursor \n
        Do: cursor.execute() (with or without params) \n
        Do: data = cursor.fetchone/fetchall OR connection.commit() - no return value \n
        Close: cursor, connection \n
        return data

        :param query:
        :param fetchone:
        :param params:
        :param commit_needed:
        :return:
        """
        pass
