from flask import request, jsonify
from model.recsys.RecSys import RecSys
from model.recsys.User import User
import hashlib


def signup_controller():
    """
    Handles the SignUpForm submission. \n
    Unsuccessful -> sends a message and status code to the frontend. \n
    Successful -> sends all the actors, genres from the database,
    and the associated user_id (which is previous max(user_id) + 1), and a status code \n
    Also, inserts the initial user information to the database.
    :return:
    """
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'password_confirmation' in request.form:
        username = request.form['username']
        password = request.form['password']
        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        password_confirmation = request.form['password_confirmation']

        if username == "":
            return jsonify({"message": "Fill in the username!"}), 401
        try:
            # Fetches database to determine if the given username is unique
            if not User.is_unique(username):
                return jsonify({"message": "This username already exists!"}), 401
            if password == "":
                return jsonify({"message": "Fill in the password!"}), 401
            if password_confirmation == "":
                return jsonify({"message": "Fill in the password confirmation!"}), 401
            if password != password_confirmation:
                return jsonify({"message": "The passwords aren't the same."}), 401

            # Fetches database for the currently maximum user_id
            user_id = User.get_max_id()

            # Inserting user data into database (id, username, password)
            user = User(user_id)
            user.insert_user(password=hashed_password, username=username)

            actors = RecSys.get_unique_actors()
            genres = RecSys.get_unique_genres()
            return jsonify(
                {
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
