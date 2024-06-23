from flask import request, jsonify
from model.recsys.Movie import Movie


def update_rating_controller():
    """
    Updates selected movie's rating for the selected user.
    :return:
    """
    try:
        # Validate request form data
        if "userId" not in request.form or "movieId" not in request.form or "rating" not in request.form:
            return jsonify({"error": "Missing 'userId', 'movieId', or 'rating' in form data."}), 400

        # extract form data
        movie_id = int(request.form["movieId"])
        user_id = int(request.form["userId"])
        rating = float(request.form["rating"])

        # update movie rating
        movie = Movie(movie_id)
        movie.update_rating(user_id=user_id, rating=rating)

        return jsonify({"message": "Rating updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
