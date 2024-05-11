from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/signup", methods=["POST"])
def signup():
    print(request.form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'password_confirmation' in request.form:
        password = request.form['password']
        password_conf = request.form['password_confirmation']
        if password != password_conf:
            return jsonify({"message": "The passwords aren't the same."})
        return jsonify({"message": "Same passwords."})
    return jsonify({'message': 'A server error has occured.'})


@app.route("/login", methods=['POST'])
def login():
    from database.mysql_constants import HOST, DBNAME, USERNAME, PASSWORD, LOGIN_SQL
    from recsys.SVDRecSys import generate_recommendation, connect_to_mysql

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        connection = connect_to_mysql(HOST, DBNAME, USERNAME, PASSWORD)
        cursor = connection.cursor()
        cursor.execute(LOGIN_SQL, (username, password))
        user_id = cursor.fetchone()
        if user_id is not None:
            user_id = user_id[0]
            recommended_movies = generate_recommendation(connection, user_id)
            return jsonify(recommended_movies)
        return jsonify({'message': 'Incorrect username or password'})
    return jsonify({'message': 'A server error has occured.'})


if __name__ == '__main__':
    app.run()
