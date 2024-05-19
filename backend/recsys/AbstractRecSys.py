from abc import ABC, abstractmethod
from typing import Union

import pandas as pd

from backend.database.Database.Database import Database
from backend.database.mysql_constants import SELECT_MOVIE_BY_ID_SQL


class AbstractRecSys(ABC):
    @classmethod
    def get_movie_by_id(cls, movie_id: int) -> Union[None, tuple]:
        query = SELECT_MOVIE_BY_ID_SQL
        cursor = Database.get_connection().cursor()
        cursor.execute(query, (movie_id,))
        movie = cursor.fetchone()
        cursor.close()
        return movie

    @staticmethod
    def movie_to_dict(movie: Union[None, tuple]) -> dict:
        if movie:
            return {
                "id": movie[0],
                "title": movie[1],
                "genres": movie[2],
                "year": movie[3],
                "director": movie[4],
                "actors": movie[5],
                "plot": movie[6],
                "poster": movie[7],
                "imdb_votes": movie[8],
                "imdb_rating": movie[9]
            }
        return {}

    @classmethod
    def get_movies_by_id_list(cls, movie_id_list: list[int]) -> list[dict]:
        movies = []
        for movie_id in movie_id_list:
            movie = cls.get_movie_by_id(movie_id)
            movie_dict = cls.movie_to_dict(movie)
            if movie_dict:
                movies.append(movie_dict)
        return movies

    @classmethod
    @abstractmethod
    def generate_recommendation(cls, user_id: [None, int] = None, actors: list = None, genres: list = None,
                                top_n: int = 15) -> list:
        pass

    @staticmethod
    def extract_genres(genres_df: pd.DataFrame) -> list[str]:
        return list(set(genre for genres in genres_df.values.tolist() for genre in genres[0].split('|') if
                        genre != "(no genres listed)"))

    @classmethod
    def get_unique_genres(cls) -> list[str]:
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
        actors_df = Database.read_mysql_to_dataframe("SELECT actors FROM movies")
        if actors_df is not None:
            return cls.extract_actors(actors_df)
        return []
