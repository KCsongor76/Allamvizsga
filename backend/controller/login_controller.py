import hashlib

from flask import request, jsonify
from backend.recsys.RecSys import RecSys
from backend.recsys.User import User


def login_controller():
    """
        Handles user login. \n
        Unsuccessful -> sends message to frontend. \n
        Successful -> generates the recommendation, and sends the movies to the frontend.
        :return:
        """
    try:
        # Validate request method and form data
        if request.method != 'POST' or 'username' not in request.form or 'password' not in request.form:
            return jsonify({"error": "Invalid request method or missing 'username' or 'password' in form data."}), 400

        username = request.form['username']
        password = request.form['password']
        hashed_received_password = hashlib.sha256(password.encode()).hexdigest()

        # Attempt to retrieve user ID from the database
        user_id = User.fetch_user_id(username=username, password=hashed_received_password)

        # If user ID exists, generate movie recommendations for the user
        if user_id is not None:
            recommended_movies = RecSys.generate_recommendation(user_id)
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
