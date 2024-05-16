import json

from flask import Flask, jsonify, request

from backend.recsys.TestRecSys import TestRecSys
from database.mysql_constants import LOGIN_SQL

app = Flask(__name__)


# TODO: sql injection, xss, ...,  prevention
# TODO: imports - lazy loading?
# TODO: MVC?
# TODO: comments, docstrings

@app.route("/signup", methods=["POST"])
def signup():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'password_confirmation' in request.form:
        username = request.form['username']
        password = request.form['password']
        password_confirmation = request.form['password_confirmation']

        if username == "":
            return jsonify(
                {
                    "message": "Fill in the username!",
                    "type": "signup",
                }
            ), 401
        try:
            connection = TestRecSys.get_connection()

            cursor = connection.cursor()
            cursor.execute("SELECT userId FROM users WHERE username = %s LIMIT 1", (username,))  # TODO: sql const
            user_id = cursor.fetchone()
            cursor.close()

            if user_id is not None:
                return jsonify({"message": "This username already exists!"})
            if password == "":
                return jsonify({"message": "Fill in the password!"})
            if password_confirmation == "":
                return jsonify({"message": "Fill in the password confirmation!"})
            if password != password_confirmation:
                return jsonify({"message": "The passwords aren't the same."})

            cursor = connection.cursor()
            cursor.execute("SELECT MAX(userId) FROM users")  # TODO: sql const
            row = cursor.fetchone()
            if row is not None:
                user_id = row[0] + 1
            else:
                user_id = 1
            cursor.close()

            actors = TestRecSys.get_unique_actors()
            genres = TestRecSys.get_unique_genres()

            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (userId, username, password) VALUES (%s, %s, %s)",  # TODO: sql const
                           (user_id, username, password))
            connection.commit()
            cursor.close()

            return jsonify(
                {
                    "type": "signup",
                    "actors": actors,
                    "genres": genres,
                }
            ), 200

        except Exception as e:
            print("Error during signup:", e)
            return jsonify(
                {
                    'message': 'A server error has occurred.',
                    "type": "signup"
                }
            ), 500  # Internal Server Error
        finally:
            TestRecSys.close_connection()
    else:
        return jsonify(
            {
                'message': 'Bad request.',
                "type": "signup"
            }
        ), 400  # Bad Request


@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        try:
            connection = TestRecSys.get_connection()
            cursor = connection.cursor()
            cursor.execute(LOGIN_SQL, (username, password))
            user_id = cursor.fetchone()
            cursor.close()
            if user_id is not None:
                user_id = user_id[0]
                recommended_movies = TestRecSys.generate_recommendation(user_id)
                return jsonify(
                    {
                        'message': 'Successful login!',
                        'movies': recommended_movies,
                        "type": "login"
                    }
                ), 200  # Successful login
            else:
                return jsonify(
                    {
                        'message': 'Incorrect username or password',
                        "type": "login"
                    }
                ), 401  # Unauthorized
        except Exception as e:
            print("Error during login:", e)
            return jsonify(
                {
                    'message': 'A server error has occurred',
                    "type": "login"
                }
            ), 500  # Internal Server Error
        finally:
            TestRecSys.close_connection()
    else:
        return jsonify(
            {
                'message': 'Bad request',
                "type": "login"
            }
        ), 400  # Bad Request


@app.route('/create_profile', methods=['POST'])
def create_profile():
    selected_data = json.loads(request.form['selectedData'])
    selected_genres = selected_data['selectedGenres']
    selected_actors = selected_data['selectedActors']

    if len(selected_actors) == 0 or len(selected_genres) == 0:
        return jsonify(
            {
                'type': 'create_profile',
                'message': 'No genres or actors selected'
            }
        ), 400

    recommended_movies = TestRecSys.generate_recommendation(actors=selected_actors, genres=selected_genres)
    return jsonify(
        {
            'type': 'create_profile',
            'message': 'Profile created successfully',
            'movies': recommended_movies,
            "genres": selected_genres,
            "actors": selected_actors
        }
    ), 200


if __name__ == '__main__':
    app.run()
