from flask import request, jsonify
from model.recsys.Movie import Movie


def get_rating_by_ids_controller():
    """
    Given the user and movie ids, returns the given rating, if exists.
    :return:
    """
    try:
        # Validate request JSON
        if "userId" not in request.json or "movieId" not in request.json:
            return jsonify({"error": "Missing 'userId' or 'movieId' in request."}), 400

        user_id = request.json["userId"]
        movie_id = request.json["movieId"]

        movie = Movie(movie_id)
        rating = movie.get_rating(user_id)

        if rating is not None:
            return jsonify({"type": "get_rating_by_ids", "rating": rating}), 200
        return jsonify({"type": "get_rating_by_ids", "message": "No rating yet"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
