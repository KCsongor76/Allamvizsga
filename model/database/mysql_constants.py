# Database credentials
HOST = "localhost"
USERNAME = "root"
PASSWORD = ""
DBNAME = "movielens_db"

# Database queries
CREATE_DB_SQL = f"CREATE DATABASE {DBNAME}"
CREATE_TABLES_SQL = """
    CREATE TABLE users (
        userId INT(11) PRIMARY KEY, 
        username VARCHAR(255),
        password VARCHAR(255),
        actors_profile VARCHAR(255),
        genres_profile VARCHAR(255)
    );
    CREATE TABLE movies (
        movieId INT(11) PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        genre VARCHAR(255) NOT NULL,
        year VARCHAR(255) NOT NULL,
        director VARCHAR(255) NOT NULL,
        actors VARCHAR(255) NOT NULL,
        plot TEXT NOT NULL,
        poster VARCHAR(255) NOT NULL,
        imdb_votes VARCHAR(255) NOT NULL,
        imdb_rating VARCHAR(255) NOT NULL
    );
    CREATE TABLE ratings (
        userId INT(11),
        movieId INT(11),
        rating DECIMAL(2,1) NOT NULL,
        timestamp TIMESTAMP NOT NULL,
        PRIMARY KEY (userId, movieId),
        FOREIGN KEY (userId) REFERENCES users(userId),
        FOREIGN KEY (movieId) REFERENCES movies(movieId)
    );
"""
INSERT_INTO_USERS_SQL = "INSERT INTO users (userId, username, password) VALUES (%s, %s, %s)"
INSERT_INTO_MOVIES_SQL = "INSERT INTO movies (movieId, title, genre, year, director, actors, plot, poster, imdb_votes, imdb_rating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
INSERT_INTO_RATINGS_SQL = "INSERT INTO ratings (userId, movieId, rating, timestamp) VALUES (%s, %s, %s, %s)"

SELECT_MOVIE_BY_ID_SQL = "SELECT movieId, title, genre, year, director, actors, plot, poster, imdb_votes, imdb_rating FROM movies WHERE movieId = %s"
SELECT_RATINGS_SQL = "SELECT userId, movieId, rating, timestamp FROM ratings"
SELECT_RATING_MOVIE_USER_ID_SQL = "SELECT rating FROM ratings WHERE movieId = %s AND userId = %s"
SELECT_STATS_BY_USER_ID = "SELECT COUNT(*), AVG(rating) FROM ratings WHERE userId = %s"
SELECT_RATED_MOVIES_BY_USER_ID_SQL = "SELECT * FROM movies INNER JOIN ratings ON movies.movieId = ratings.movieId WHERE ratings.userId = %s"
SELECT_MAX_USER_ID_SQL = "SELECT MAX(userId) FROM users"
SELECT_USER_ID_BY_USERNAME_SQL = "SELECT userId FROM users WHERE username = %s LIMIT 1"
SELECT_USERNAME_BY_USER_ID_SQL = "SELECT username FROM users WHERE userId = %s"
SELECT_PROFILE_DATA_BY_USER_ID_SQL = "SELECT actors_profile, genres_profile FROM users WHERE userId = %s"
SELECT_MOST_POPULAR_RECOMMENDATIONS_SQL = "SELECT * FROM movies ORDER BY imdb_rating DESC LIMIT %s"
LOGIN_SQL = "SELECT userId FROM users WHERE username = %s AND password = %s"

UPDATE_PROFILE_SQL = "UPDATE users SET actors_profile = %s, genres_profile = %s WHERE userId = %s"
UPDATE_RATINGS_SQL = "UPDATE ratings SET rating = %s, timestamp = %s WHERE userId = %s AND movieId = %s"

DELETE_RATING_SQL = "DELETE FROM ratings WHERE userId = %s AND movieId = %s"
DELETE_DUPE_RATINGS_SQL = "DELETE FROM ratings WHERE movieId IN (2851, 4051, 4241, 5264, 5672, 6003, 6776, 32600, 66511, 79677, 95771, 107780, 127194, 174551, 183197, 183227);"
DELETE_DUPE_MOVIES_SQL = "DELETE FROM movies WHERE title = '#DUPE#'"
