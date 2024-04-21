import random

import mysql.connector
import numpy as np
import pandas as pd
from surprise import SVD, Reader, Dataset
from surprise.model_selection import cross_validate
from backend.database.mysql_constants import HOST, DBNAME, USERNAME, PASSWORD, SELECT_MOVIE_BY_ID_SQL, \
    SELECT_RATINGS_SQL
from backend.recsys.Movie import Movie


def connect_to_mysql(host, database, user, password):
    try:
        connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        if connection.is_connected():
            return connection
    except Exception as e:
        print("Error connecting to MySQL:", e)
        return None


def read_mysql_to_dataframe(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=columns)
        return df
    except Exception as e:
        print("Error executing MySQL query:", e)
        return None


def get_movie_by_id(id):
    connection = connect_to_mysql(HOST, DBNAME, USERNAME, PASSWORD)
    cursor = connection.cursor()
    cursor.execute(SELECT_MOVIE_BY_ID_SQL, (id,))
    movie = cursor.fetchone()
    cursor.close()
    connection.close()
    return movie


def get_movies_by_id_list(ids: list[int]):
    connection = connect_to_mysql(HOST, DBNAME, USERNAME, PASSWORD)
    cursor = connection.cursor()
    movies = []
    for id in ids:
        cursor.execute(SELECT_MOVIE_BY_ID_SQL, (id,))
        movie = cursor.fetchone()
        movie_obj = Movie(movie[1], movie[2], movie[3], movie[4], movie[5], movie[6], movie[7], movie[8], movie[9])
        movie_dict = movie_obj.to_dict()
        print(movie_dict)
        movies.append(movie_dict)
    cursor.close()
    connection.close()
    return movies


def generate_recommendation(connection, user_id, top_n=15):
    np.random.seed(0)
    random.seed(0)

    ratings_df = read_mysql_to_dataframe(connection, SELECT_RATINGS_SQL)
    connection.close()  # Close the connection when done

    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(ratings_df[['userId', 'movieId', 'rating']], reader)
    algo = SVD()
    # Perform cross-validation
    cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

    # Train the algorithm on the whole dataset
    trainset = data.build_full_trainset()
    algo.fit(trainset)

    movie_ids = list(trainset.all_items())

    # Get the list of movies the user has already rated
    rated_movies = [rating[0] for rating in trainset.ur[user_id]]

    # Remove the rated movies from the list of all movie IDs
    unrated_movies = [movie_id for movie_id in movie_ids if movie_id not in rated_movies]

    # Predict ratings for the unrated movies
    predictions = [algo.predict(user_id, movie_id) for movie_id in unrated_movies]

    # Sort the predictions by estimated rating in descending order
    predictions.sort(key=lambda x: x.est, reverse=True)

    # Get the top N recommendations
    top_movies = predictions[:top_n]

    # Print the top recommended movies
    print(f"Top {top_n} Recommendations for User {user_id}:")

    ids = []
    for i, movie in enumerate(top_movies):
        ids.append(movie.iid)

    recommended_movies = get_movies_by_id_list(ids)
    return recommended_movies


# connection = connect_to_mysql(HOST, DBNAME, USERNAME, PASSWORD)
#
# if connection.is_connected():
#     recommended_movies = generate_recommendation(connection, user_id=1)
