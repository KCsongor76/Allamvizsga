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
from backend.database.mysql_constants import SELECT_RATINGS_SQL, SELECT_MOST_POPULAR_RECOMMENDATIONS_SQL
from backend.recsys.AbstractRecSys import AbstractRecSys
from pathlib import Path

from backend.recsys.Movie import Movie
from backend.recsys.User import User


class RecSys(AbstractRecSys):

    @classmethod
    def tfidf_recommender(cls, user_id: int, movies: pd.DataFrame, genres: str, actors: str, top_n: int = 15):

        rated_movies = Movie.get_rated_movies_by_user_id(user_id)
        rated_movie_ids = [movie['id'] for movie in rated_movies]

        # Step 1: Combine genres and actors into a single 'tags' column
        movies['tags'] = movies['genre'] + ' ' + movies['actors']

        genres = ' '.join(genres.split('|'))
        actors = ' '.join(actors.split('|'))
        # Step 2: Create a query string from the input genres and actors
        query = genres + ' ' + actors
        query = ' '.join(query.split())  # Ensure there's no extraneous whitespace
        print(f"Query: {query}")

        # Step 3: Vectorize the 'tags' column
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(movies['tags'])

        # Step 4: Vectorize the query
        query_vec = tfidf.transform([query])
        print(f"query vec: {query_vec}")

        # Step 5: Compute cosine similarity between the query and the movies
        cosine_sim = cosine_similarity(query_vec, tfidf_matrix).flatten()

        # Step 6: Get the top N movie indices
        top_indices = [idx for idx in cosine_sim.argsort()[::-1] if movies.iloc[idx]['id'] not in rated_movie_ids]
        print(f"Top indices: {top_indices}")

        # Step 7: Get the top N movie IDs
        top_movie_ids = movies.iloc[top_indices[:top_n]]['id'].values
        print(f"Top movie ids: {top_movie_ids}")

        recommended_movies = Movie.get_movies_by_id_list(top_movie_ids.tolist())
        print(f"recommended movies: {recommended_movies}")
        return recommended_movies

    @staticmethod
    def handle_dumping_loading(model, combined_features):
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
        print(f"rec_movies_df: {combined_recommendations}")
        recommended_movies = []
        for movieId in combined_recommendations['id'].tolist():
            if movieId not in all_rated_movie_ids:
                movie = Database.db_process(query="SELECT * FROM movies WHERE movieId = %s", params=(movieId,))
                if movie:
                    recommended_movies.append(Movie.movie_to_dict(movie))
        return recommended_movies[:top_n]

    @classmethod
    def collaborative_filter_recommender(cls, algo_class, params, user_id: int, top_n: int = 10) -> list[dict]:
        print("collaborative")
        np.random.seed(0)
        random.seed(0)

        ratings_df = Database.read_mysql_to_dataframe(query=SELECT_RATINGS_SQL)
        print(f"ratings_df: {ratings_df}")
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(ratings_df[['userId', 'movieId', 'rating']], reader)

        algo = algo_class(**params)
        cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)
        trainset = data.build_full_trainset()
        algo.fit(trainset)

        # Get the list of all movie IDs in the trainset
        movie_internal_ids = list(trainset.all_items())
        movie_ids = [trainset.to_raw_iid(internal_id) for internal_id in movie_internal_ids]
        print(f"movie_ids: {movie_ids}")

        # Get the list of rated movies for the user
        try:
            user_internal_id = trainset.to_inner_uid(user_id)
            rated_internal_movies = [rating[0] for rating in trainset.ur[user_internal_id]]
            rated_movies = [trainset.to_raw_iid(internal_id) for internal_id in rated_internal_movies]
        except ValueError:
            # If the user_id is not in the trainset, handle accordingly
            rated_movies = []

        print(f"rated_movies: {rated_movies}")

        # Get the list of unrated movies for the user
        unrated_internal_movies = [internal_id for internal_id in movie_internal_ids if
                                   internal_id not in rated_internal_movies]
        predictions = [algo.predict(user_id, trainset.to_raw_iid(internal_id)) for internal_id in
                       unrated_internal_movies]
        predictions.sort(key=lambda x: x.est, reverse=True)
        top_movies = predictions[:top_n]
        print(f"top_movies: {top_movies}")

        ids = [movie.iid for movie in top_movies]
        print(f"ids: {ids}")

        # Verify that no rated movies are included in the final recommendation
        ids = [movie_id for movie_id in ids if movie_id not in rated_movies]

        recommended_movies = Movie.get_movies_by_id_list(ids)
        return recommended_movies

    @classmethod
    def cold_start_user_recommendation(cls, user_id: int, actors: str = None,
                                       genres: str = None, top_n: int = 10) -> list[dict]:
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
                tf_ifd_movies = cls.tfidf_recommender(user_id=user_id, movies=all_movies, genres=genres, actors=actors,
                                                      top_n=5)
                recommended_movies = list(tf_ifd_movies) + list(popular_movies_dict)[:5]
                return recommended_movies
            else:
                print("popular + tf-idf + sbert")
                tf_idf_movies = cls.tfidf_recommender(user_id=user_id, movies=all_movies, genres=genres, actors=actors,
                                                      top_n=2)
                sbert_movies = cls.sbert_recommender(user_id=user_id, generated_movies=popular_movies_dict, top_n=3)
                recommended_movies = list(sbert_movies) + list(tf_idf_movies) + list(popular_movies_dict)[:5]
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
            tf_idf_movies = cls.tfidf_recommender(user_id=user_id, movies=all_movies, genres=genres, actors=actors,
                                                  top_n=2)
            # TODO: TF-IDF - already rated movies
            sbert_movies = cls.sbert_recommender(user_id=user_id, generated_movies=rated_movies, top_n=2)
            recommended_movies = list(sbert_movies) + list(tf_idf_movies) + list(collaborative_movies)

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
            tf_idf_movies = cls.tfidf_recommender(user_id=user_id, movies=all_movies, genres=genres, actors=actors,
                                                  top_n=2)
            # TODO: TF-IDF - already rated movies
            sbert_movies = cls.sbert_recommender(user_id=user_id, generated_movies=rated_movies, top_n=2)
            recommended_movies = list(sbert_movies) + list(tf_idf_movies) + list(collaborative_movies)

        return recommended_movies

    @classmethod
    def generate_recommendation(cls, user_id: int, top_n: int = 10) -> list[dict]:
        user = User(user_id)
        count, avg = user.get_user_stats()
        actors, genres = user.get_user_profile()

        print(f"count: {count}")
        print(f"actors: {actors}, type: {type(actors)}")
        print(f"genres: {genres}, type: {type(genres)}")
        # TODO: colliding movies check
        if count in range(0, 26):
            recommended_movies = cls.cold_start_user_recommendation(user_id=user_id, actors=actors, genres=genres,
                                                                    top_n=top_n)
        elif count in range(26, 150):
            recommended_movies = cls.moderately_active_user_recommendation(user_id=user_id, actors=actors,
                                                                           genres=genres)
        else:
            recommended_movies = cls.highly_active_user_recommendation(user_id=user_id, actors=actors, genres=genres)
        return recommended_movies
