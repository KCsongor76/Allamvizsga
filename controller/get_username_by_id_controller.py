from flask import request, jsonify
from model.recsys.User import User


def get_username_by_id_controller():
    """
    Returns the username by the given user id.
    :return:
    """
    try:
        # Validate request JSON
        if "userId" not in request.json:
            return jsonify({"error": "Missing 'userId' in request."}), 400
        user_id = request.json["userId"]

        user = User(user_id)
        username = user.get_username()

        if username:
            return jsonify({"message": "Username fetched successfully!", "username": username}), 200
        else:
            return jsonify({"error": "User not found."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
