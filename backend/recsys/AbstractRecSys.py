from abc import ABC, abstractmethod
import mysql.connector
import pandas as pd
from backend.database.mysql_constants import HOST, DBNAME, USERNAME, PASSWORD, SELECT_MOVIE_BY_ID_SQL


# TODO: separate database operations


class AbstractRecSys(ABC):
    _connection = None

    @classmethod
    def connect_to_mysql(cls):
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
    def get_connection(cls):
        if cls._connection is None or not cls._connection.is_connected():
            cls.connect_to_mysql()
        return cls._connection

    @classmethod
    def close_connection(cls):
        try:
            if cls._connection is not None and cls._connection.is_connected():
                # Consume any unread results
                while cls._connection.next_result():
                    pass
                cls._connection.close()
        except Exception as e:
            print("Error closing connection:", e)
        finally:
            # Reset the connection attribute to None
            cls._connection = None

    @classmethod
    def read_mysql_to_dataframe(cls, query):
        try:
            cursor = cls.get_connection().cursor()
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
            cursor.close()
            return pd.DataFrame(data, columns=columns)
        except Exception as e:
            print("Error executing MySQL query:", e)
            return None

    @classmethod
    def get_movie_by_id(cls, id):
        query = SELECT_MOVIE_BY_ID_SQL
        cursor = cls.get_connection().cursor()
        cursor.execute(query, (id,))
        movie = cursor.fetchone()
        cursor.close()
        return movie

    @staticmethod
    def movie_to_dict(movie):
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
    def get_movies_by_id_list(cls, ids: list[int]):
        movies = []
        for id in ids:
            movie = cls.get_movie_by_id(id)
            movie_dict = cls.movie_to_dict(movie)
            if movie_dict:
                movies.append(movie_dict)
        return movies

    @classmethod
    @abstractmethod
    def generate_recommendation(cls, user_id, actors=None, genres=None, top_n=15):
        pass

    @staticmethod
    def extract_genres(genres_df):
        return list(set(genre for genres in genres_df.values.tolist() for genre in genres[0].split('|') if
                        genre != "(no genres listed)"))

    @classmethod
    def get_unique_genres(cls):
        genres_df = cls.read_mysql_to_dataframe("SELECT genre FROM movies")
        if genres_df is not None:
            return cls.extract_genres(genres_df)
        return []
        # ['IMAX', 'Drama', 'Mystery', 'Comedy', 'Sci-Fi', 'Thriller', 'Horror', 'War', 'Children', 'Animation',
        # 'Adventure', 'Western', 'Film-Noir', 'Action', 'Documentary', 'Fantasy', 'Romance', 'Musical', 'Crime']

    @staticmethod
    def extract_actors(actors_df):
        return list(set(actor.strip() for actors in actors_df.values.tolist() for actor in actors[0].split(',')))

    @classmethod
    def get_unique_actors(cls):
        actors_df = cls.read_mysql_to_dataframe("SELECT actors FROM movies")
        if actors_df is not None:
            return cls.extract_actors(actors_df)
        return []
