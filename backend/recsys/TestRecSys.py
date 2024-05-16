import random
from abc import ABC

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate

from backend.database.mysql_constants import SELECT_RATINGS_SQL
from backend.recsys.AbstractRecSys import AbstractRecSys


class TestRecSys(AbstractRecSys, ABC):

    @staticmethod
    def prepare_movies(movies_df):
        movies = pd.DataFrame()
        movies['id'] = movies_df['movieId']
        movies['title'] = movies_df['title']
        movies['year'] = movies_df['year']
        movies['genre'] = movies_df['genre'].apply(lambda x: x.replace('|', ' '))
        movies['director'] = movies_df['director'].str.replace(' ', '').str.replace(',', ' ')
        movies['actors'] = movies_df['actors'].str.replace(' ', '').str.replace(',', ' ')
        movies['tags'] = movies['genre'] + ' ' + movies['actors']
        movies.fillna('', inplace=True)
        movies = movies[['id', 'title', 'genre', 'actors', 'tags']]

        return movies

    @staticmethod
    def get_similarities_tfidf(movies):
        tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
        vectorized_data = tfidf.fit_transform(movies['tags'])
        similarity = cosine_similarity(vectorized_data)
        return similarity

    @classmethod
    def contents_based_recommender(cls, movies, genres, actors, how_many=15):
        # TODO: not good enough
        # Convert actors array to a single string without spaces
        actors = ' '.join([actor.replace(' ', '') for actor in actors])
        # Calculate TF-IDF similarities
        similarity_matrix = cls.get_similarities_tfidf(movies)
        given_genres = genres
        # Filter movies by genres
        relevant_movies = movies[movies['genre'].apply(lambda x: all(genre in x for genre in given_genres))]
        # Filter further by actors
        relevant_movies = relevant_movies[relevant_movies['actors'].str.contains(actors)]
        # Get indices of relevant movies
        movie_indices = relevant_movies.index
        # Calculate mean similarity score for each movie
        mean_similarity_scores = similarity_matrix[movie_indices].mean(axis=0)
        # Get indices of top recommended movies
        top_indices = mean_similarity_scores.argsort()[::-1][:how_many]
        print(top_indices.tolist())
        # Get detailed movie data using movie IDs
        recommended_movies = cls.get_movies_by_id_list(top_indices.tolist())
        print(f"recommended movies: {recommended_movies}")
        return recommended_movies

    @classmethod
    def generate_recommendation(cls, user_id=None, actors=None, genres=None, top_n=15):
        connection = cls.get_connection()
        if connection:
            try:
                if user_id is None:
                    movies_df = cls.read_mysql_to_dataframe(query="SELECT * FROM movies")
                    movies = cls.prepare_movies(movies_df)
                    recommended_movies = cls.contents_based_recommender(movies, genres, actors)
                    return recommended_movies
                else:
                    print("collaborative")
                    np.random.seed(0)
                    random.seed(0)

                    ratings_df = cls.read_mysql_to_dataframe(query=SELECT_RATINGS_SQL)
                    reader = Reader(rating_scale=(1, 5))
                    data = Dataset.load_from_df(ratings_df[['userId', 'movieId', 'rating']], reader)

                    algo = SVD()
                    cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)
                    trainset = data.build_full_trainset()
                    algo.fit(trainset)
                    movie_ids = list(trainset.all_items())

                    rated_movies = [rating[0] for rating in trainset.ur[user_id]]
                    unrated_movies = [movie_id for movie_id in movie_ids if movie_id not in rated_movies]
                    predictions = [algo.predict(user_id, movie_id) for movie_id in unrated_movies]
                    predictions.sort(key=lambda x: x.est, reverse=True)
                    top_movies = predictions[:top_n]

                    print(f"Top {top_n} Recommendations for User {user_id}:")
                    ids = []
                    for i, movie in enumerate(top_movies):
                        ids.append(movie.iid)
                    recommended_movies = cls.get_movies_by_id_list(ids)
                    print(f"recommended movies: {recommended_movies}")
                    return recommended_movies
            finally:
                cls.close_connection()
        else:
            print("Failed to connect to MySQL.")
            return []
