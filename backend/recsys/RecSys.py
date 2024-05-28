import os
import pickle
import random
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Reader, Dataset, SVD, KNNBaseline
from surprise.model_selection import cross_validate
from backend.database.Database.Database import Database
from backend.database.mysql_constants import SELECT_RATINGS_SQL, SELECT_STATS_BY_USER_ID, \
    SELECT_MOST_POPULAR_RECOMMENDATIONS_SQL, SELECT_PROFILE_DATA_BY_USER_ID_SQL
from backend.recsys.AbstractRecSys import AbstractRecSys
from pathlib import Path


class RecSys(AbstractRecSys):

    @staticmethod
    def get_similarities_tfidf(movies: pd.DataFrame) -> list:
        tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
        vectorized_data = tfidf.fit_transform(movies['tags'])
        similarity = cosine_similarity(vectorized_data)
        return similarity

    @classmethod
    def tfidf_recommender(cls, movies: pd.DataFrame, genres: list, actors: list, how_many: int = 15) -> list:
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
    def content_based_recommender(cls, movies: pd.DataFrame,
                                  genres: list = None,
                                  actors: list = None,
                                  top_n: int = 10) -> list[dict]:

        print("content based")
        movies['combined_features'] = movies['genre'] + ' ' + movies['actors']
        combined_features = np.array(movies['combined_features'])

        model = SentenceTransformer('all-MiniLM-L6-v2')
        current_path = Path(__file__).parent.resolve()
        # path = Path(__file__).parent.resolve() / 'SBERT_data/embeddings_g_a.pkl'
        sbert_path = current_path / 'SBERT_data'
        file_path = sbert_path / 'embeddings_g_a.pkl'
        # Check if the path exists
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                combined_embeddings = pickle.load(f)
            similarity_sbert_combined = cosine_similarity(combined_embeddings)
            cos_sim_data_combined = pd.DataFrame(similarity_sbert_combined)
        else:
            # Assuming model and combined_features are defined elsewhere in the actual code
            combined_embeddings = model.encode(combined_features, show_progress_bar=True)
            similarity_sbert_combined = cosine_similarity(combined_embeddings)
            cos_sim_data_combined = pd.DataFrame(similarity_sbert_combined)

            # Create directory if it doesn't exist
            sbert_path.mkdir(parents=True, exist_ok=True)
            # dir_path.parent.mkdir(parents=True, exist_ok=True)

            # Save embeddings to a file using pickle
            with open(sbert_path / 'embeddings_g_a.pkl', 'wb') as f:
                pickle.dump(combined_embeddings, f)

            # Save similarity_sbert to a file using pickle
            with open(sbert_path / 'similarity_sbert_g_a.pkl', 'wb') as f:
                pickle.dump(similarity_sbert_combined, f)

            # Save cos_sim_data to a file using pickle
            with open(sbert_path / 'cos_sim_data_g_a.pkl', 'wb') as f:
                pickle.dump(cos_sim_data_combined, f)

        # Prepare data for recommendations
        data = movies[['title', 'genre']]
        indices = pd.Series(movies.index, index=movies['title'])

        def get_recommendations(genres: list[str], actors: list[str], top_n: int = 10):
            print("content - get_recommendations")
            # TODO: fix movieId/title problem - fetchone()
            # Create a query string from the genres and actors lists
            query = ' '.join(genres) + ' ' + ' '.join(actors)
            # Encode the query string using SBERT
            query_embedding = model.encode([query])
            # Compute similarity between the query embedding and all movie embeddings
            query_sim_scores = cosine_similarity(query_embedding, combined_embeddings).flatten()
            # Get the top N most similar movie indices
            sim_scores = list(enumerate(query_sim_scores))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[:top_n]
            movie_indices = [i[0] for i in sim_scores]
            final_data = data.iloc[movie_indices]
            titles = final_data['title'].tolist()
            movies = []
            for _title in titles:
                movie = Database.db_process(query="SELECT * FROM movies WHERE title = %s",
                                            params=(_title,))
                movies.append(RecSys.movie_to_dict(movie))
            return movies

        recommended_movies = get_recommendations(genres, actors, top_n)
        return recommended_movies

    @classmethod
    def collaborative_filter_recommender(cls, algo_class, params, user_id: int, top_n: int = 10) -> list[dict]:
        print("collaborative")
        np.random.seed(0)
        random.seed(0)

        ratings_df = Database.read_mysql_to_dataframe(query=SELECT_RATINGS_SQL)
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(ratings_df[['userId', 'movieId', 'rating']], reader)

        algo = algo_class(**params)
        cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)
        trainset = data.build_full_trainset()
        algo.fit(trainset)
        movie_ids = list(trainset.all_items())

        rated_movies = [rating[0] for rating in trainset.ur[user_id]]
        unrated_movies = [movie_id for movie_id in movie_ids if movie_id not in rated_movies]
        predictions = [algo.predict(user_id, movie_id) for movie_id in unrated_movies]
        predictions.sort(key=lambda x: x.est, reverse=True)
        top_movies = predictions[:top_n]

        ids = []
        for i, movie in enumerate(top_movies):
            ids.append(movie.iid)
        recommended_movies = cls.get_movies_by_id_list(ids)
        return recommended_movies

    @classmethod
    def cold_start_user_recommendation(cls, actors: list = None, genres: list = None, top_n: int = 10) -> list[dict]:
        print("coldstart")
        popular_movies = Database.db_process(query=SELECT_MOST_POPULAR_RECOMMENDATIONS_SQL,
                                             params=(top_n,),
                                             fetchone=False)
        popular_movies_dict = []
        for movie in popular_movies:
            popular_movies_dict.append(cls.movie_to_dict(movie))

        if actors is None and genres is None:
            print("only popular")
            return popular_movies_dict
        else:
            movies_df = Database.read_mysql_to_dataframe(query="SELECT * FROM movies")
            movies = cls.prepare_movies(movies_df)
            content_based_movies = cls.content_based_recommender(movies, genres, actors, 5)
            recommended_movies = list(content_based_movies) + list(popular_movies_dict)[:5]
            return recommended_movies

    @classmethod
    def moderately_active_user_recommendation(cls, user_id: int,
                                              actors: None | list[str] = None,
                                              genres: None | list[str] = None) -> list[dict]:
        print("moderately")
        # jupyter notebook - grid_search_with_figs
        knn_user_params = {'k': 40, 'sim_options': {'name': 'msd', 'min_support': 3, 'user_based': True},
                           'bsl_options': {'method': 'sgd'}}
        collaborative_movies = cls.collaborative_filter_recommender(algo_class=KNNBaseline, params=knn_user_params,
                                                                    user_id=user_id, top_n=10)
        recommended_movies = collaborative_movies
        # if actors is not None and genres is not None:
        #     print("profile yes")
        #     movies_df = Database.read_mysql_to_dataframe(query="SELECT * FROM movies")
        #     movies = cls.prepare_movies(movies_df)
        #     content_based_movies = cls.content_based_recommender(movies=movies, top_n=4)
        #     recommended_movies += content_based_movies
        return recommended_movies

    @classmethod
    def highly_active_user_recommendation(cls, user_id: int,
                                          actors: None | list[str] = None,
                                          genres: None | list[str] = None) -> list[dict]:
        print("highly")
        # jupyter notebook - grid_search_with_figs
        svd_params = {'n_factors': 160, 'n_epochs': 100, 'lr_all': 0.008, 'reg_all': 0.1}
        collaborative_movies = cls.collaborative_filter_recommender(algo_class=SVD, params=svd_params,
                                                                    user_id=user_id, top_n=10)
        recommended_movies = collaborative_movies
        # if actors is not None and genres is not None:
        #     print("profile yes")
        #     movies_df = Database.read_mysql_to_dataframe(query="SELECT * FROM movies")
        #     movies = cls.prepare_movies(movies_df)
        #     content_based_movies = cls.content_based_recommender(movies=movies, top_n=4)
        #     recommended_movies += content_based_movies
        return recommended_movies

    @classmethod
    def generate_recommendation(cls, user_id: int, top_n: int = 10) -> list[dict]:
        user_stats = Database.db_process(query=SELECT_STATS_BY_USER_ID, params=(user_id,))
        user_profile = Database.db_process(query=SELECT_PROFILE_DATA_BY_USER_ID_SQL, params=(user_id,))
        count = user_stats[0]
        actors = user_profile[0]
        genres = user_profile[1]

        print(f"count: {count}")
        print(f"actors: {actors}")
        print(f"genres: {genres}")
        # TODO: colliding movies check
        # TODO: don't recommend if already rated
        if count in range(0, 26):
            recommended_movies = cls.cold_start_user_recommendation(actors=actors, genres=genres, top_n=top_n)
        elif count in range(26, 150):
            recommended_movies = cls.moderately_active_user_recommendation(user_id=user_id, actors=actors,
                                                                           genres=genres)
        else:
            recommended_movies = cls.highly_active_user_recommendation(user_id=user_id, actors=actors, genres=genres)
        return recommended_movies
