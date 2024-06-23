from model.database.Database.Database import Database
from model.database.mysql_constants import SELECT_STATS_BY_USER_ID, SELECT_PROFILE_DATA_BY_USER_ID_SQL, \
    INSERT_INTO_USERS_SQL, SELECT_USER_ID_BY_USERNAME_SQL, SELECT_MAX_USER_ID_SQL, LOGIN_SQL, UPDATE_PROFILE_SQL, \
    SELECT_USERNAME_BY_USER_ID_SQL


class User:
    def __init__(self, user_id: int):
        self.__user_id: int = user_id

    def get_user_id(self) -> int:
        return self.__user_id

    def insert_user(self, username: str, password: str) -> None:
        """
        Inserts a new user into the database with the provided username and password.

        Parameters:
            username (str): The username of the new user.
            password (str): The password of the new user.

        Returns:
            None
        """

        Database.db_process(query=INSERT_INTO_USERS_SQL,
                            params=(self.__user_id, username, password),
                            fetchone=False,
                            commit_needed=True)

    def update_user_stats(self, actors: str, genres: str) -> None:
        """
        Updates the user's statistics with the provided actors and genres.

        Parameters:
            actors (str): The actors associated with the user.
            genres (str): The genres associated with the user.

        Returns:
            None
        """

        Database.db_process(query=UPDATE_PROFILE_SQL,
                            params=(actors, genres, self.__user_id),
                            fetchone=False,
                            commit_needed=True)

    def get_username(self) -> str:
        """
        Get the username associated with the user ID.

        :return: str - The username of the user.
        """

        username = Database.db_process(query=SELECT_USERNAME_BY_USER_ID_SQL, params=(self.__user_id,))
        username = username[0]
        return username

    def get_user_stats(self):
        """
        Retrieves the user's statistics from the database.

        Returns:
            tuple: A tuple containing the count of records and the average rating.
        """

        user_stats = Database.db_process(query=SELECT_STATS_BY_USER_ID, params=(self.__user_id,))
        count = user_stats[0]
        if count == 0:
            return count, 0
        avg = float(user_stats[1])
        return count, avg

    def get_user_profile(self):
        """
        Retrieves the user's profile data from the database.

        Returns:
            tuple: A tuple containing the user's actors and genres.
        """

        user_profile = Database.db_process(query=SELECT_PROFILE_DATA_BY_USER_ID_SQL, params=(self.__user_id,))
        actors = user_profile[0]
        genres = user_profile[1]
        return actors, genres

    @staticmethod
    def is_unique(username: str) -> bool:
        """
        Check if the username is unique in the database.

        Parameters:
            username (str): The username to check for uniqueness.

        Returns:
            bool: True if the username is unique, False otherwise.
        """

        user_id = Database.db_process(query=SELECT_USER_ID_BY_USERNAME_SQL, params=(username,))
        if user_id is None:
            return True
        return False

    @staticmethod
    def get_max_id() -> int:
        """
        Retrieves the maximum user ID from the database.

        Returns:
            int: The maximum user ID incremented by 1 if it exists, otherwise returns 1.
        """

        max_id = Database.db_process(query=SELECT_MAX_USER_ID_SQL)
        if max_id is not None:
            return max_id[0] + 1
        return 1

    @staticmethod
    def fetch_user_id(username: str, password: str) -> int | None:
        """
        Retrieves the user ID based on the provided username and password.

        Parameters:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            int | None: The user ID if found, None otherwise.
        """

        user_id = Database.db_process(query=LOGIN_SQL, params=(username, password))
        if user_id is not None:
            return user_id[0]
        return user_id

    def __str__(self) -> str:
        """
        Returns a string representation of the User object containing the user ID and username.
        :return: str - The string representation of the User object.
        """

        return f"{self.get_user_id()}: {self.get_username()}"

# if __name__ == "__main__":
#     user = User(611)
