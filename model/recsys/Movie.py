import datetime

import pandas as pd

from model.database.Database.Database import Database
from model.database.mysql_constants import SELECT_MOVIE_BY_ID_SQL, INSERT_INTO_RATINGS_SQL, UPDATE_RATINGS_SQL, \
    SELECT_RATED_MOVIES_BY_USER_ID_SQL, SELECT_RATING_MOVIE_USER_ID_SQL, DELETE_RATING_SQL


class Movie:
    def __init__(self, movie_id: int):
        self.__movie_id: int = movie_id

    def get_movie_id(self):
        return self.__movie_id

    def add_rating(self, user_id: int, rating: float) -> None:
        current_time = datetime.datetime.now()
        timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
        Database.db_process(query=INSERT_INTO_RATINGS_SQL,
                            params=(user_id, self.__movie_id, rating, timestamp),
                            fetchone=False,
                            commit_needed=True)

    def delete_rating(self, user_id: int) -> None:
        Database.db_process(query=DELETE_RATING_SQL,
                            params=(user_id, self.__movie_id),
                            fetchone=False,
                            commit_needed=True)

    def update_rating(self, user_id: int, rating: float) -> None:
        current_time = datetime.datetime.now()
        timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
        Database.db_process(query=UPDATE_RATINGS_SQL,
                            params=(rating, timestamp, user_id, self.__movie_id),
                            fetchone=False,
                            commit_needed=True)

    def get_rating(self, user_id: int) -> float | None:
        rating = Database.db_process(query=SELECT_RATING_MOVIE_USER_ID_SQL, params=(self.__movie_id, user_id))
        if rating is not None:
            return float(rating[0])
        return rating

    @staticmethod
    def prepare_movies(movies_df: pd.DataFrame) -> pd.DataFrame:
        movies = pd.DataFrame()
        movies['id'] = movies_df['movieId']
        movies['title'] = movies_df['title']
        movies['year'] = movies_df['year']
        movies['genre'] = movies_df['genre'].apply(lambda x: x.replace('|', ' '))
        movies['director'] = movies_df['director'].str.replace(' ', '').str.replace(',', ' ')
        movies['actors'] = movies_df['actors'].str.replace(' ', '').str.replace(',', ' ')
        movies['plot'] = movies_df['plot'].fillna('')
        movies.isnull().sum()  # TODO: ???
        movies.fillna('', inplace=True)
        movies = movies[['id', 'title', 'genre', 'actors', 'plot']]
        return movies

    @classmethod
    def get_movies_from_mysql(cls) -> pd.DataFrame:
        movies_df = Database.read_mysql_to_dataframe(query="SELECT * FROM movies")
        movies = cls.prepare_movies(movies_df)
        return movies

    @staticmethod
    def get_movie_by_id(movie_id: int) -> None | tuple:
        """
        Fetches the database for a movie by a given movieId, and returns the movie.
        :param movie_id:
        :return:
        """
        movie = Database.db_process(query=SELECT_MOVIE_BY_ID_SQL, params=(movie_id,))
        return movie

    @staticmethod
    def movie_to_dict(movie: None | tuple) -> dict:
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
        """
        Fetches the database multiple times for movies given a list of movieIds,
        and return a list of movies (type dict).
        :param movie_id_list:
        :return:
        """
        movies = []
        for movie_id in movie_id_list:
            movie = cls.get_movie_by_id(movie_id)
            movie_dict = cls.movie_to_dict(movie)
            if movie_dict:
                movies.append(movie_dict)
        return movies

    @classmethod
    def get_rated_movies_by_user_id(cls, user_id: int) -> list[dict]:
        movies = Database.db_process(query=SELECT_RATED_MOVIES_BY_USER_ID_SQL, params=(user_id,), fetchone=False)
        # Convert movie data to dictionary format
        movies_list = [Movie.movie_to_dict(movie) for movie in movies]
        return movies_list
