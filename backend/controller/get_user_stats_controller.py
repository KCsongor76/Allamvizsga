from flask import request, jsonify
from backend.recsys.Movie import Movie
from backend.recsys.User import User


def get_user_stats_controller():
    """
    Returns some stats from the user's profile, activity.
    :return:
    """
    try:
        # Validate request JSON
        if "userId" not in request.json:
            return jsonify({"error": "Missing 'userId' in request."}), 400
        user_id = request.json["userId"]

        user = User(user_id)
        actors, genres = user.get_user_profile()
        count, avg = user.get_user_stats()

        if count == 0:
            return jsonify({"message": "No rated movies.", "actors": actors, "genres": genres}), 200

        movies_list = Movie.get_rated_movies_by_user_id(user_id=user_id)

        return jsonify({
            "message": "User stats fetched successfully.",
            "actors": actors,
            "genres": genres,
            "movies": movies_list,
            "stats": {"count": count, "avg": avg}
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
