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
from model.database.Database.Database import Database
from model.database.mysql_constants import SELECT_RATINGS_SQL, SELECT_MOST_POPULAR_RECOMMENDATIONS_SQL
from model.recsys.AbstractRecSys import AbstractRecSys
from pathlib import Path

from model.recsys.Movie import Movie
from model.recsys.User import User


class RecSys(AbstractRecSys):

    @classmethod
    def tfidf_recommender(cls, all_movies, genres, actors, top_n=5):
        """
        Perform TF-IDF vectorization on movie tags based on genres and actors to recommend top similar movies.

        Parameters:
            all_movies (DataFrame): DataFrame containing movie information.
            genres (str): Pipe-separated string of genres.
            actors (str): Pipe-separated string of actors.
            top_n (int): Number of top recommendations to return.

        Returns:
            list: List of dictionaries representing the recommended movies.
        """

        # Ensure genres are formatted correctly
        genres = genres.replace('|', ' ')

        # Ensure actors are formatted correctly
        actors = ' '.join(actor.replace(' ', '') for actor in actors.split('|'))

        # Combine genres and actors into a single string
        input_tags = f"{genres} {actors}"
        all_movies['tags'] = all_movies['genre'] + ' ' + all_movies['actors']

        # TF-IDF Vectorization
        tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
        vectorized_data = tfidf.fit_transform(all_movies['tags'])

        # Transform the input_tags
        input_vector = tfidf.transform([input_tags])

        # Calculate cosine similarity between input_vector and all movies
        similarity = cosine_similarity(input_vector, vectorized_data)

        # Get similarity scores
        sim_scores_all = list(enumerate(similarity[0]))
        sim_scores_all = sorted(sim_scores_all, key=lambda x: x[1], reverse=True)

        if top_n > 0:
            sim_scores_all = sim_scores_all[:top_n]

        # Get the movie indices of the top similar movies
        movie_indices = [i[0] for i in sim_scores_all]
        scores = [i[1] for i in sim_scores_all]

        # Return the top n most similar movies from the movies df
        top_titles_df = pd.DataFrame(all_movies.iloc[movie_indices]['title'])
        top_titles_df['sim_scores'] = scores
        top_titles_df['ranking'] = range(1, len(top_titles_df) + 1)

        recommended_movies = []
        for title in top_titles_df['title']:
            movie = Database.db_process(query="SELECT * FROM movies WHERE title = %s", params=(title,), fetchone=True)
            recommended_movies.append(Movie.movie_to_dict(movie))
        return recommended_movies

    @staticmethod
    def handle_dumping_loading(model, combined_features):
        """
        A function that handles the dumping and loading of embeddings.
        It checks if a file path exists, loads the embeddings if it does,
        and encodes the combined features using the model if the file path does not exist.

        Parameters:
            model: The model used for encoding.
            combined_features: The combined features to be encoded.

        Returns:
            The combined embeddings after loading or encoding.
        """

        current_path = Path(__file__).parent.resolve()
        sbert_path = current_path / 'SBERT_data'
        file_path = sbert_path / 'embeddings_g_a.pkl'

        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                combined_embeddings = pickle.load(f)
        else:
            combined_embeddings = model.encode(combined_features, show_progress_bar=True)
            sbert_path.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'wb') as f:
                pickle.dump(combined_embeddings, f)

        return combined_embeddings

    @classmethod
    def sbert_recommender(cls, user_id: int, top_n: int = 10, generated_movies: list[dict] = None) -> list[dict]:
        """
        Recommends top similar movies using SBERT embeddings for a given user.

        Args:
            user_id (int): The ID of the user for whom recommendations are generated.
            top_n (int, optional): Number of top recommendations to return. Defaults to 10.
            generated_movies (list[dict], optional): Movies to not include in recommendations.
            Defaults to None.

        Returns:
            list[dict]: List of dictionaries representing the recommended movies.
        """

        movies = Movie.get_movies_from_mysql()
        rated_movies = Movie.get_rated_movies_by_user_id(user_id=user_id)
        # rated_movie_ids = [movie['id'] for movie in rated_movies]

        rated_movie_ids = []
        threshold = 3
        for movie in rated_movies:
            movie_instance = Movie(movie_id=movie['id'])
            rating = movie_instance.get_rating(user_id=user_id)
            if rating >= threshold:
                rated_movie_ids.append(movie['id'])

        all_rated_movies = list(rated_movies) + list(generated_movies)
        all_rated_movie_ids = [movie['id'] for movie in all_rated_movies]

        text_data = np.array(movies['plot'])

        model = SentenceTransformer('all-MiniLM-L6-v2')

        embeddings = cls.handle_dumping_loading(model, text_data)
        similarity = cosine_similarity(embeddings)
        cos_sim_data = pd.DataFrame(similarity)

        data = movies[['id', 'title', 'genre']]
        indices = pd.Series(movies.index, index=movies['id'])

        def get_sbert_recommendations(movie_id: int) -> pd.DataFrame:
            """
            Get SBERT recommendations for a given movie ID.

            Parameters:
                movie_id (int): The ID of the movie for which recommendations are generated.

            Returns:
                pd.DataFrame: DataFrame containing recommended movies and their similarity scores.
            """

            idx = indices[movie_id]

            sim_scores = list(enumerate(cos_sim_data[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:top_n + 1]

            movie_indices = [i[0] for i in sim_scores]
            sim_scores = pd.DataFrame(sim_scores, columns=['index', 'similarity_score'])

            final_data = data.iloc[movie_indices]
            final_data = final_data.merge(sim_scores, left_index=True, right_on='index')
            final_data['similarity_score'] = round(final_data['similarity_score'], 2)
            del final_data['index']
            return final_data

        combined_recommendations = pd.DataFrame()
        for rated_movie_id in rated_movie_ids:
            rec_movies_df = get_sbert_recommendations(rated_movie_id)
            combined_recommendations = pd.concat([combined_recommendations, rec_movies_df])

        combined_recommendations = combined_recommendations.drop_duplicates(subset='id')
        combined_recommendations = combined_recommendations.sort_values(by='similarity_score', ascending=False)
        recommended_movies = []
        for movieId in combined_recommendations['id'].tolist():
            if movieId not in all_rated_movie_ids:
                movie = Database.db_process(query="SELECT * FROM movies WHERE movieId = %s", params=(movieId,))
                if movie:
                    recommended_movies.append(Movie.movie_to_dict(movie))
        return recommended_movies[:top_n]

    @classmethod
    def collaborative_filter_recommender(cls, algo_class, params, user_id: int, top_n: int = 10) -> list[dict]:
        """
        A collaborative filtering recommender function that uses the provided algorithm class
        and parameters to recommend movies to a user.

        Parameters:
            algo_class: The class of the collaborative filtering algorithm to be used.
            params: Parameters for the collaborative filtering algorithm.
            user_id (int): The ID of the user for whom recommendations are generated.
            top_n (int, optional): Number of top recommendations to return. Defaults to 10.

        Returns:
            list[dict]: List of dictionaries representing the recommended movies.
        """

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

        # Get the list of all movie IDs in the trainset
        movie_internal_ids = list(trainset.all_items())

        # Get the list of rated movies for the user
        rated_internal_movies = []
        try:
            user_internal_id = trainset.to_inner_uid(user_id)
            rated_internal_movies = [rating[0] for rating in trainset.ur[user_internal_id]]
            rated_movies = [trainset.to_raw_iid(internal_id) for internal_id in rated_internal_movies]
        except ValueError:
            # If the user_id is not in the trainset, handle accordingly
            rated_movies = []

        # Get the list of unrated movies for the user
        unrated_internal_movies = [internal_id for internal_id in movie_internal_ids if
                                   internal_id not in rated_internal_movies]
        predictions = [algo.predict(user_id, trainset.to_raw_iid(internal_id)) for internal_id in
                       unrated_internal_movies]
        predictions.sort(key=lambda x: x.est, reverse=True)
        top_movies = predictions[:top_n]

        ids = [movie.iid for movie in top_movies]

        # Verify that no rated movies are included in the final recommendation
        ids = [movie_id for movie_id in ids if movie_id not in rated_movies]

        recommended_movies = Movie.get_movies_by_id_list(ids)
        return recommended_movies

    @classmethod
    def cold_start_user_recommendation(cls, user_id: int, actors: str = None,
                                       genres: str = None, top_n: int = 10) -> list[dict]:
        """
        Perform cold start user recommendation based on user's profile information or popular movies.

        Parameters:
            user_id (int): The ID of the user for whom recommendations are generated.
            actors (str, optional): Pipe-separated string of actors in the user's profile. Defaults to None.
            genres (str, optional): Pipe-separated string of genres in the user's profile. Defaults to None.
            top_n (int, optional): Number of top recommendations to return. Defaults to 10.

        Returns:
            list[dict]: List of dictionaries representing the recommended movies.
        """

        print("coldstart")
        has_profile = actors is not None and genres is not None
        rated_movies = Movie.get_rated_movies_by_user_id(user_id)

        threshold = 3
        threshold_ok_movies = []
        for movie in rated_movies:
            movie_instance = Movie(movie_id=movie['id'])
            rating = movie_instance.get_rating(user_id=user_id)
            if rating >= threshold:
                threshold_ok_movies.append(movie)

        popular_movies = Database.db_process(query=SELECT_MOST_POPULAR_RECOMMENDATIONS_SQL,
                                             params=(top_n,),
                                             fetchone=False)

        popular_movies_dict = []
        for movie in popular_movies:
            movie_dict = Movie.movie_to_dict(movie)
            if movie_dict not in rated_movies:
                popular_movies_dict.append(movie_dict)

        if not has_profile:
            if len(threshold_ok_movies) == 0:
                print("only popular")
                return popular_movies_dict
            else:
                print("popular + sbert")
                sbert_movies = cls.sbert_recommender(user_id=user_id, generated_movies=popular_movies_dict, top_n=5)
                recommended_movies = list(sbert_movies) + list(popular_movies_dict)[:5]
                return recommended_movies
        else:
            all_movies = Movie.get_movies_from_mysql()
            print(f"first moviedata: {all_movies['actors']}")
            if len(threshold_ok_movies) == 0:
                print("popular + tf-idf")
                tf_idf_movies = cls.tfidf_recommender(all_movies=all_movies, genres=genres, actors=actors, top_n=5)
                recommended_movies = list(tf_idf_movies) + list(popular_movies_dict)[:5]
                return recommended_movies
            else:
                print("popular + tf-idf + sbert")
                tf_idf_movies = cls.tfidf_recommender(all_movies=all_movies, genres=genres, actors=actors, top_n=2)
                sbert_movies = cls.sbert_recommender(user_id=user_id, generated_movies=popular_movies_dict, top_n=3)
                recommended_movies = list(sbert_movies) + list(tf_idf_movies) + list(popular_movies_dict)[:5]
                return recommended_movies

    @classmethod
    def moderately_active_user_recommendation(cls, user_id: int,
                                              actors: None | str = None,
                                              genres: None | str = None) -> list[dict]:
        """
        Perform moderately active user recommendation based on collaborative filtering with optional actors and genres.

        Parameters:
            user_id (int): The ID of the user for whom recommendations are generated.
            actors (None | list[str], optional): List of actors the user is interested in. Defaults to None.
            genres (None | list[str], optional): List of genres the user prefers. Defaults to None.

        Returns:
            list[dict]: List of dictionaries representing the recommended movies for the moderately active user.
        """

        print("moderately")
        # jupyter notebook - grid_search_with_figs
        knn_user_params = {'k': 40, 'sim_options': {'name': 'msd', 'min_support': 3, 'user_based': True},
                           'bsl_options': {'method': 'sgd'}}
        collaborative_movies = cls.collaborative_filter_recommender(algo_class=KNNBaseline, params=knn_user_params,
                                                                    user_id=user_id, top_n=6)

        rated_movies = Movie.get_rated_movies_by_user_id(user_id)
        has_profile = actors is not None and genres is not None
        rated_movies += collaborative_movies
        if not has_profile:
            print("KNN + SBERT")
            sbert_movies = cls.sbert_recommender(user_id=user_id, generated_movies=rated_movies, top_n=4)
            recommended_movies = list(sbert_movies) + list(collaborative_movies)
        else:
            print("KNN + TFIDF + SBERT")
            all_movies = Movie.get_movies_from_mysql()
            tf_idf_movies = cls.tfidf_recommender(all_movies=all_movies, genres=genres, actors=actors, top_n=2)
            sbert_movies = cls.sbert_recommender(user_id=user_id, generated_movies=rated_movies, top_n=2)
            recommended_movies = list(sbert_movies) + list(tf_idf_movies) + list(collaborative_movies)

        return recommended_movies

    @classmethod
    def highly_active_user_recommendation(cls, user_id: int,
                                          actors: None | str = None,
                                          genres: None | str = None) -> list[dict]:
        """
        Recommends movies for highly active users based on collaborative filtering and content-based techniques.

        Parameters:
            user_id (int): The ID of the user for whom recommendations are generated.
            actors (None, list[str], optional): List of actors the user likes. Defaults to None.
            genres (None, list[str], optional): List of genres the user prefers. Defaults to None.

        Returns:
            list[dict]: List of dictionaries representing the recommended movies for the user.
        """

        print("highly")
        # jupyter notebook - grid_search_with_figs
        svd_params = {'n_factors': 160, 'n_epochs': 100, 'lr_all': 0.008, 'reg_all': 0.1}
        collaborative_movies = cls.collaborative_filter_recommender(algo_class=SVD, params=svd_params,
                                                                    user_id=user_id, top_n=6)
        rated_movies = Movie.get_rated_movies_by_user_id(user_id)
        has_profile = actors is not None and genres is not None
        rated_movies += collaborative_movies
        if not has_profile:
            print("SVD + SBERT")
            sbert_movies = cls.sbert_recommender(user_id=user_id, generated_movies=rated_movies, top_n=4)
            recommended_movies = list(sbert_movies) + list(collaborative_movies)
        else:
            print("SVD + TFIDF + SBERT")
            all_movies = Movie.get_movies_from_mysql()
            tf_idf_movies = cls.tfidf_recommender(all_movies=all_movies, genres=genres, actors=actors, top_n=2)
            sbert_movies = cls.sbert_recommender(user_id=user_id, generated_movies=rated_movies, top_n=2)
            recommended_movies = list(sbert_movies) + list(tf_idf_movies) + list(collaborative_movies)

        return recommended_movies

    @classmethod
    def generate_recommendation(cls, user_id: int, top_n: int = 10) -> list[dict]:
        """
        Generate recommendations for a user based on their user stats, profile, and activity level.

        Parameters:
            user_id (int): The ID of the user for whom recommendations are generated.
            top_n (int, optional): Number of top recommendations to return. Defaults to 10.

        Returns:
            list[dict]: List of dictionaries representing the recommended movies for the user.
        """

        user = User(user_id)
        count, avg = user.get_user_stats()
        actors, genres = user.get_user_profile()

        if count in range(0, 26):
            recommended_movies = cls.cold_start_user_recommendation(user_id=user_id, actors=actors, genres=genres,
                                                                    top_n=top_n)
        elif count in range(26, 150):
            recommended_movies = cls.moderately_active_user_recommendation(user_id=user_id, actors=actors,
                                                                           genres=genres)
        else:
            recommended_movies = cls.highly_active_user_recommendation(user_id=user_id, actors=actors, genres=genres)
        return recommended_movies
