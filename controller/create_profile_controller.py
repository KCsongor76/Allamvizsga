import json
from flask import request, jsonify
from model.recsys.RecSys import RecSys
from model.recsys.User import User


def create_profile_controller():
    """
    After successful sign up, and choosing the genres and actors on the frontend,
    handles these submitted data. \n
    Unsuccessful -> if no actors or genres are selected
    Successful -> based on the created user profile, generates the recommendation list,
    inserts user data into database.
    :return:
    """
    try:
        if "selectedData" not in request.form:
            return jsonify({"error": "Missing 'selectedData' in form data."}), 400

        selected_data = json.loads(request.form['selectedData'])
        selected_genres = selected_data['selectedGenres']
        selected_actors = selected_data['selectedActors']
        user_id = selected_data['userId']
        # Check if genres or actors are selected
        if not selected_actors or not selected_genres:
            return jsonify({"message": "No genres or actors selected"}), 400

        actors = '|'.join(selected_actors)
        genres = '|'.join(selected_genres)

        # Update user profile in the database
        user = User(user_id)
        user.update_user_stats(actors=actors, genres=genres)

        # Generate movie recommendations based on selected genres and actors
        recommended_movies = RecSys.generate_recommendation(user_id=user_id)

        return jsonify({
            'message': 'Profile created successfully',
            'movies': recommended_movies,
            "genres": selected_genres,
            "actors": selected_actors,
            "user_id": user_id
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
