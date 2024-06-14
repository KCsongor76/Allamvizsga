from flask import request, jsonify
from model.recsys.Movie import Movie


def add_rating_controller():
    """
    Adds rating to selected movie by selected user.
    :return:
    """
    try:
        # Validate request form data
        if "userId" not in request.form or "movieId" not in request.form or "rating" not in request.form:
            return jsonify({"error": "Missing 'userId', 'movieId', or 'rating' in form data."}), 400

        movie_id = int(request.form["movieId"])
        user_id = int(request.form["userId"])
        rating = float(request.form["rating"])

        movie = Movie(movie_id)
        movie.add_rating(user_id=user_id, rating=rating)

        return jsonify({"message": "Rating added successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
