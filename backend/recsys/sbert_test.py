import pickle

import pandas as pd

from backend.database.Database.Database import Database
from backend.recsys.Movie import Movie


def get_recommendations(indices, cos_sim_data, data, title, top_n):
    idx = indices[title]
    sim_scores = list(enumerate(cos_sim_data[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n + 1]
    movie_indices = [i[0] for i in sim_scores]
    final_data = data.iloc[movie_indices]
    titles = final_data['title'].tolist()

    movies = []
    for _title in titles:
        movie = Database.db_process(query="SELECT * FROM movies WHERE title = %s",
                                    params=(_title,))
        movies.append(Movie.movie_to_dict(movie))
    return movies


# def content_based_recommender(cls, movies: pd.DataFrame,
#                               genres: list = None,
#                               actors: list = None,
#                               top_n: int = 10) -> list[dict]:
#     # Load cos_sim_data from the saved file
#     from pathlib import Path
#     path = Path(__file__).parent.resolve() / 'SBERT_data/cos_sim_data.pkl'
#     with open(path, 'rb') as f:
#         cos_sim_data = pickle.load(f)
#
#     data = movies[['title', 'genre']]
#     indices = pd.Series(movies.index, index=movies['title'])
#     title = "Star Wars: Episode III - Revenge of the Sith"
#     recommended_movies = cls.get_recommendations(indices, cos_sim_data, data, title, top_n)
#     return recommended_movies


# def cold_start_user_recommendation(cls, actors: list = None, genres: list = None, top_n: int = 10) -> list[dict]:
#     popular_movies = Database.db_process(query=SELECT_MOST_POPULAR_RECOMMENDATIONS_SQL, params=(top_n,), fetchone=False)
#     popular_movies_dict = []
#     for movie in popular_movies:
#         popular_movies_dict.append(cls.movie_to_dict(movie))
#
#     if actors is None and genres is None:
#         return popular_movies_dict
#     else:
#         movies_df = Database.read_mysql_to_dataframe(query="SELECT * FROM movies")
#         movies = cls.prepare_movies(movies_df)
#         content_based_movies = cls.content_based_recommender(movies, genres, actors, 5)
#         recommended_movies = list(content_based_movies) + list(popular_movies_dict)
#         return recommended_movies


movies = Database.read_mysql_to_dataframe("SELECT * FROM movies")
# Load cos_sim_data from the saved file
from pathlib import Path

path = Path(__file__).parent.resolve() / 'SBERT_data/cos_sim_data.pkl'
with open(path, 'rb') as f:
    cos_sim_data = pickle.load(f)

data = movies[['title', 'genre']]
indices = pd.Series(movies.index, index=movies['title'])
title = "Star Wars: Episode III - Revenge of the Sith"
recommended_movies = get_recommendations(indices, cos_sim_data, data, title, 5)
print(recommended_movies)
