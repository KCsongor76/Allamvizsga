import datetime
import json

from flask import Flask, jsonify, request

from backend.database.Database.Database import Database
from backend.recsys.AbstractRecSys import AbstractRecSys
from backend.recsys.TestRecSys import TestRecSys
from database.mysql_constants import *

app = Flask(__name__)


# TODO: sql injection, xss, ...,  prevention

@app.route("/signup", methods=["POST"])
def signup():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'password_confirmation' in request.form:
        username = request.form['username']
        password = request.form['password']
        password_confirmation = request.form['password_confirmation']

        if username == "":
            return jsonify({"message": "Fill in the username!"}), 401
        try:
            user_id = Database.db_process(query=SELECT_USER_ID_BY_USERNAME_SQL, params=(username,))
            if user_id is not None:
                return jsonify({"message": "This username already exists!"}), 401
            if password == "":
                return jsonify({"message": "Fill in the password!"}), 401
            if password_confirmation == "":
                return jsonify({"message": "Fill in the password confirmation!"}), 401
            if password != password_confirmation:
                return jsonify({"message": "The passwords aren't the same."}), 401

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
            return jsonify({'message': 'A server error has occurred.'}), 500  # Internal Server Error
    else:
        return jsonify({'message': 'Bad request.'}), 400  # Bad Request


@app.route("/login", methods=['POST'])
def login():
    try:
        # Validate request method and form data
        if request.method != 'POST' or 'username' not in request.form or 'password' not in request.form:
            return jsonify({"error": "Invalid request method or missing 'username' or 'password' in form data."}), 400

        username = request.form['username']
        password = request.form['password']

        # Attempt to retrieve user ID from the database
        user_id = Database.db_process(query=LOGIN_SQL, params=(username, password), fetchone=True)

        # If user ID exists, generate movie recommendations for the user
        if user_id:
            user_id = user_id[0]
            recommended_movies = TestRecSys.generate_recommendation(user_id)
            return jsonify({
                'message': 'Successful login!',
                'movies': recommended_movies,
                'user_id': user_id,
            }), 200  # Successful login
        else:
            return jsonify({'message': 'Incorrect username or password'}), 401  # Unauthorized

    except Exception as e:
        print("Error during login:", e)
        return jsonify({'message': 'A server error has occurred'}), 500  # Internal Server Error


@app.route('/create_profile', methods=['POST'])
def create_profile():
    try:
        # Validate request form data
        if "selectedData" not in request.form:
            return jsonify({"error": "Missing 'selectedData' in form data."}), 400

        selected_data = json.loads(request.form['selectedData'])
        selected_genres = selected_data['selectedGenres']
        selected_actors = selected_data['selectedActors']
        user_id = selected_data['userId']  # TODO: coding convention... (user_id vs userId from React) ?

        # Check if genres or actors are selected
        if not selected_actors or not selected_genres:
            return jsonify({"message": "No genres or actors selected"}), 400

        # Generate movie recommendations based on selected genres and actors
        recommended_movies = TestRecSys.generate_recommendation(actors=selected_actors, genres=selected_genres)

        # Format selected genres and actors
        actors = ' '.join([actor.replace(' ', '') for actor in selected_actors])
        genres = ' '.join([genre.replace(' ', '') for genre in selected_genres])

        # Update user profile in the database
        Database.db_process(query=UPDATE_PROFILE_SQL,
                            params=(actors, genres, user_id),
                            fetchone=False,
                            commit_needed=True)

        return jsonify({
            'message': 'Profile created successfully',
            'movies': recommended_movies,
            "genres": selected_genres,
            "actors": selected_actors,
            "user_id": user_id
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/update_rating", methods=["PUT"])
def update_rating():
    try:
        # Validate request form data
        if "userId" not in request.form or "movieId" not in request.form or "rating" not in request.form:
            return jsonify({"error": "Missing 'userId', 'movieId', or 'rating' in form data."}), 400

        movie_id = request.form["movieId"]
        user_id = request.form["userId"]
        rating = float(request.form["rating"])
        current_time = datetime.datetime.now()
        timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')

        # Update rating in the database
        Database.db_process(query=UPDATE_RATINGS_SQL,
                            params=(rating, timestamp, user_id, movie_id),
                            fetchone=False,
                            commit_needed=True)

        return jsonify({"message": "Rating updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/delete_rating", methods=["DELETE"])
def delete_rating():
    try:
        # Validate request form data
        if "userId" not in request.form or "movieId" not in request.form:
            return jsonify({"error": "Missing 'userId' or 'movieId' in form data."}), 400

        movie_id = request.form["movieId"]
        user_id = request.form["userId"]

        # Delete rating from the database
        Database.db_process(query=DELETE_RATING_SQL,
                            params=(user_id, movie_id),
                            fetchone=False,
                            commit_needed=True)
        return jsonify({"message": "Rating deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/add_rating", methods=["POST"])
def add_rating():
    try:
        # Validate request form data
        if "userId" not in request.form or "movieId" not in request.form or "rating" not in request.form:
            return jsonify({"error": "Missing 'userId', 'movieId', or 'rating' in form data."}), 400

        movie_id = request.form["movieId"]
        user_id = request.form["userId"]
        rating = float(request.form["rating"])
        current_time = datetime.datetime.now()
        timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')

        # Add rating to the database
        Database.db_process(query=INSERT_INTO_RATINGS_SQL,
                            params=(user_id, movie_id, rating, timestamp),
                            fetchone=False,
                            commit_needed=True)

        return jsonify({"message": "Rating added successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get_rating_by_ids", methods=["POST"])
def get_rating_by_ids():
    try:
        # Validate request JSON
        if "userId" not in request.json or "movieId" not in request.json:
            return jsonify({"error": "Missing 'userId' or 'movieId' in request."}), 400

        user_id = request.json["userId"]
        movie_id = request.json["movieId"]
        # Fetch rating from the database
        rating = Database.db_process(query=SELECT_RATING_MOVIE_USER_ID_SQL, params=(movie_id, user_id))

        # If rating exists, convert it to float
        if rating is not None:
            rating = float(rating[0])

        # Return the rating if it's a float or an integer
        if isinstance(rating, (float, int)):
            return jsonify({"type": "get_rating_by_ids", "rating": rating}), 200

        # If no rating found, return a message
        return jsonify({"type": "get_rating_by_ids", "message": "No rating yet"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get_username_by_id", methods=["POST"])
def get_username_by_id():
    try:
        # Validate request JSON
        if "userId" not in request.json:
            return jsonify({"error": "Missing 'userId' in request."}), 400
        user_id = request.json["userId"]

        # Fetch username from the database
        username = Database.db_process(query=SELECT_USERNAME_BY_USER_ID_SQL, params=(user_id,))
        if username:
            return jsonify({"message": "Username fetched successfully!", "username": username}), 200
        else:
            return jsonify({"error": "User not found."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get_user_stats", methods=["POST"])
def get_user_stats():
    try:
        # Validate request JSON
        if "userId" not in request.json:
            return jsonify({"error": "Missing 'userId' in request."}), 400

        user_id = request.json["userId"]

        # Fetch profile data from the database
        profile_data = Database.db_process(query=SELECT_PROFILE_DATA_BY_USER_ID_SQL, params=(user_id,))
        actors, genres = profile_data[0], profile_data[1]

        # Fetch stats data from the database
        stats_data = Database.db_process(query=SELECT_STATS_BY_USER_ID, params=(user_id,))
        count = stats_data[0]
        # If no rated movies, return with profile data only
        if count == 0:
            return jsonify({"message": "No rated movies.", "actors": actors, "genres": genres}), 200
        avg = float(stats_data[1])

        # Fetch rated movies
        movies = Database.db_process(query=SELECT_RATED_MOVIES_BY_USER_ID_SQL, params=(user_id,), fetchone=False)
        # Convert movie data to dictionary format
        movies_list = [AbstractRecSys.movie_to_dict(movie) for movie in movies]

        return jsonify({
            "message": "User stats fetched successfully.",
            "actors": actors,
            "genres": genres,
            "movies": movies_list,
            "stats": {"count": count, "avg": avg}
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run()
