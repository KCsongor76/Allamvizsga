from abc import ABC, abstractmethod
import pandas as pd

from backend.database.Database.Database import Database


class AbstractRecSys(ABC):
    @classmethod
    @abstractmethod
    def generate_recommendation(cls, user_id: int, top_n: int = 10) -> list:
        pass

    @staticmethod
    def extract_genres(genres_df: pd.DataFrame) -> list[str]:
        return list(set(genre for genres in genres_df.values.tolist() for genre in genres[0].split('|') if
                        genre != "(no genres listed)"))

    @classmethod
    def get_unique_genres(cls) -> list[str]:
        """
        Fetches the database for all genres, and returns every unique genre
        in a list via the extract_genres class method.
        :return:
        """
        genres_df = Database.read_mysql_to_dataframe("SELECT genre FROM movies")
        if genres_df is not None:
            return cls.extract_genres(genres_df)
        return []
        # ['IMAX', 'Drama', 'Mystery', 'Comedy', 'Sci-Fi', 'Thriller', 'Horror', 'War', 'Children', 'Animation',
        # 'Adventure', 'Western', 'Film-Noir', 'Action', 'Documentary', 'Fantasy', 'Romance', 'Musical', 'Crime']

    @staticmethod
    def extract_actors(actors_df: pd.DataFrame) -> list[str]:
        return list(set(actor.strip() for actors in actors_df.values.tolist() for actor in actors[0].split(',')))

    @classmethod
    def get_unique_actors(cls) -> list[str]:
        """
        Fetches the database for all actors, and returns every unique actor
        in a list via the extract_actors class method.
        :return:
        """
        actors_df = Database.read_mysql_to_dataframe("SELECT actors FROM movies")
        if actors_df is not None:
            return cls.extract_actors(actors_df)
        return []
