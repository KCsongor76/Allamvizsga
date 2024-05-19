import datetime
import json

from flask import Flask, jsonify, request

from backend.database.Database.Database import Database
from backend.recsys.AbstractRecSys import AbstractRecSys
from backend.recsys.TestRecSys import TestRecSys
from database.mysql_constants import *

app = Flask(__name__)


# TODO: sql injection, xss, ...,  prevention
# TODO: imports - lazy loading?
# TODO: MVC?
# TODO: comments, docstrings

@app.route("/signup", methods=["POST"])
def signup():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'password_confirmation' in request.form:
        username = request.form['username']
        password = request.form['password']
        password_confirmation = request.form['password_confirmation']

        if username == "":
            return jsonify(
                {
                    "message": "Fill in the username!",
                    "type": "signup",
                }
            ), 401
        try:
            user_id = Database.db_process(query=SELECT_USER_ID_BY_USERNAME_SQL, params=(username,), )

            if user_id is not None:
                return jsonify(
                    {
                        "message": "This username already exists!",
                        "type": "signup"
                    }
                ), 401
            if password == "":
                return jsonify(
                    {
                        "message": "Fill in the password!",
                        "type": "signup"
                    }
                ), 401
            if password_confirmation == "":
                return jsonify(
                    {
                        "message": "Fill in the password confirmation!",
                        "type": "signup"
                    }
                ), 401
            if password != password_confirmation:
                return jsonify(
                    {
                        "message": "The passwords aren't the same.",
                        "type": "signup"
                    }
                ), 401

            row = Database.db_process(query=SELECT_MAX_USER_ID_SQL)
            if row is not None:
                user_id = row[0] + 1
            else:
                user_id = 1

            actors = TestRecSys.get_unique_actors()
            genres = TestRecSys.get_unique_genres()

            Database.db_process(query=INSERT_INTO_USERS_SQL,
                                params=(user_id, username, password),
                                fetchone=False,
                                commit_needed=True)

            return jsonify(
                {
                    "type": "signup",
                    "actors": actors,
                    "genres": genres,
                    "user_id": user_id
                }
            ), 200

        except Exception as e:
            print("Error during signup:", e)
            return jsonify(
                {
                    'message': 'A server error has occurred.',
                    "type": "signup"
                }
            ), 500  # Internal Server Error
        finally:
            Database.close_connection()
    else:
        return jsonify(
            {
                'message': 'Bad request.',
                "type": "signup"
            }
        ), 400  # Bad Request


@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        try:
            user_id = Database.db_process(query=LOGIN_SQL, params=(username, password), )

            if user_id is not None:
                user_id = user_id[0]
                recommended_movies = TestRecSys.generate_recommendation(user_id)
                return jsonify(
                    {
                        'message': 'Successful login!',
                        'movies': recommended_movies,
                        'user_id': user_id,
                        "type": "login"
                    }
                ), 200  # Successful login
            else:
                return jsonify(
                    {
                        'message': 'Incorrect username or password',
                        "type": "login"
                    }
                ), 401  # Unauthorized
        except Exception as e:
            print("Error during login:", e)
            return jsonify(
                {
                    'message': 'A server error has occurred',
                    "type": "login"
                }
            ), 500  # Internal Server Error
        finally:
            Database.close_connection()
    else:
        return jsonify(
            {
                'message': 'Bad request',
                "type": "login"
            }
        ), 400  # Bad Request


@app.route('/create_profile', methods=['POST'])
def create_profile():
    selected_data = json.loads(request.form['selectedData'])
    print(f"selected data: {selected_data}")
    selected_genres = selected_data['selectedGenres']
    selected_actors = selected_data['selectedActors']
    user_id = selected_data['userId']
    # TODO: coding convention... (user_id vs userId from React) ?

    if len(selected_actors) == 0 or len(selected_genres) == 0:
        return jsonify(
            {
                'type': 'create_profile',
                'message': 'No genres or actors selected'
            }
        ), 400

    recommended_movies = TestRecSys.generate_recommendation(actors=selected_actors, genres=selected_genres)
    actors = ' '.join([actor.replace(' ', '') for actor in selected_actors])
    genres = ' '.join([genre.replace(' ', '') for genre in selected_genres])
    # TODO: not good enough

    Database.db_process(query=UPDATE_PROFILE_SQL,
                        params=(actors, genres, user_id),
                        fetchone=False,
                        commit_needed=True)

    return jsonify(
        {
            'type': 'create_profile',
            'message': 'Profile created successfully',
            'movies': recommended_movies,
            "genres": selected_genres,
            "actors": selected_actors,
            "user_id": user_id
        }
    ), 200


@app.route("/update_rating", methods=["PUT"])
def update_rating():
    movie_id = request.form["movieId"]
    user_id = request.form["userId"]
    rating = float(request.form["rating"])
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')

    Database.db_process(query=UPDATE_RATINGS_SQL,
                        params=(rating, timestamp, user_id, movie_id),
                        fetchone=False,
                        commit_needed=True)
    return jsonify({"message": "Rating updated successfully"}), 200


@app.route("/delete_rating", methods=["DELETE"])
def delete_rating():
    movie_id = request.form["movieId"]
    user_id = request.form["userId"]

    Database.db_process(query=DELETE_RATING_SQL,
                        params=(user_id, movie_id),
                        fetchone=False,
                        commit_needed=True)
    return jsonify({"message": "Rating deleted successfully"}), 200


@app.route("/add_rating", methods=["POST"])
def add_rating():
    movie_id = request.form["movieId"]
    user_id = request.form["userId"]
    rating = float(request.form["rating"])
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')

    Database.db_process(query=INSERT_INTO_RATINGS_SQL,
                        params=(user_id, movie_id, rating, timestamp),
                        fetchone=False,
                        commit_needed=True)
    return jsonify({"message": "Rating added successfully"}), 200


@app.route("/get_rating_by_ids", methods=["POST"])
def get_rating_by_ids():
    movie_id = request.json["movieId"]
    user_id = request.json["userId"]
    rating = Database.db_process(query=SELECT_RATING_MOVIE_USER_ID_SQL, params=(movie_id, user_id))

    if rating is not None:
        rating = float(rating[0])
    if type(rating) is float or type(rating) is int:
        return jsonify(
            {
                "type": "get_rating_by_ids",
                "rating": rating
            }
        ), 200
    return jsonify(
        {
            "type": "get_rating_by_ids",
            "message": "no rating yet"
        }
    ), 200


@app.route("/get_username_by_id", methods=["POST"])
def get_username_by_id():
    user_id = request.json["userId"]
    username = Database.db_process(query=SELECT_USERNAME_BY_USER_ID_SQL, params=(user_id,))

    print(user_id, username[0])
    return jsonify(
        {
            "message": "Username fetched successfully!",
            "username": username[0]
        }
    ), 200


@app.route("/get_user_stats", methods=["POST"])
def get_user_stats():
    user_id = request.json["userId"]
    profile_data = Database.db_process(query=SELECT_PROFILE_DATA_BY_USER_ID_SQL, params=(user_id,))

    actors = profile_data[0]
    genres = profile_data[1]
    data = Database.db_process(query=SELECT_STATS_BY_USER_ID, params=(user_id,))

    count = data[0]
    if count == 0:
        return jsonify(
            {
                "message": "No rated movies.",
                "actors": actors,
                "genres": genres,
            }
        ), 200
    avg = float(data[1])
    movies = Database.db_process(query=SELECT_RATED_MOVIES_BY_USER_ID_SQL, params=(user_id,), fetchone=False)
    movies_list = []
    for movie in movies:
        movie_dict = AbstractRecSys.movie_to_dict(movie)
        print(movie_dict)
        movies_list.append(movie_dict)

    Database.close_connection()
    return jsonify(
        {
            "message": "alma",
            "actors": actors,
            "genres": genres,
            "movies": movies_list,
            "stats": {
                "count": count,
                "avg": avg
            }
        }
    ), 200


if __name__ == '__main__':
    app.run()
