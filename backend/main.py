from flask import Flask

from controller.signup_controller import signup_controller
from controller.create_profile_controller import create_profile_controller
from controller.login_controller import login_controller
from controller.update_rating_controller import update_rating_controller
from controller.delete_rating_controller import delete_rating_controller
from controller.add_rating_controller import add_rating_controller
from controller.get_rating_by_ids_controller import get_rating_by_ids_controller
from controller.get_username_by_id_controller import get_username_by_id_controller
from controller.get_user_stats_controller import get_user_stats_controller

app = Flask(__name__)


# TODO: sql injection, xss, ...,  prevention
# TODO: password hash

@app.route("/signup", methods=["POST"])
def signup():
    return signup_controller()


@app.route('/create_profile', methods=['POST'])
def create_profile():
    return create_profile_controller()


@app.route("/login", methods=['POST'])
def login():
    return login_controller()


@app.route("/update_rating", methods=["PUT"])
def update_rating():
    return update_rating_controller()


@app.route("/delete_rating", methods=["DELETE"])
def delete_rating():
    return delete_rating_controller()


@app.route("/add_rating", methods=["POST"])
def add_rating():
    return add_rating_controller()


@app.route("/get_rating_by_ids", methods=["POST"])
def get_rating_by_ids():
    return get_rating_by_ids_controller()


@app.route("/get_username_by_id", methods=["POST"])
def get_username_by_id():
    return get_username_by_id_controller()


@app.route("/get_user_stats", methods=["POST"])
def get_user_stats():
    return get_user_stats_controller()


if __name__ == '__main__':
    app.run()
