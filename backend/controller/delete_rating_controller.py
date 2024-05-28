from flask import request, jsonify
from backend.recsys.Movie import Movie


def delete_rating_controller():
    """
    Deletes selected movie's rating for the selected user.
    :return:
    """
    try:
        # Validate request form data
        if "userId" not in request.form or "movieId" not in request.form:
            return jsonify({"error": "Missing 'userId' or 'movieId' in form data."}), 400

        movie_id = int(request.form["movieId"])
        user_id = int(request.form["userId"])

        movie = Movie(movie_id)
        movie.delete_rating(user_id)
        return jsonify({"message": "Rating deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
