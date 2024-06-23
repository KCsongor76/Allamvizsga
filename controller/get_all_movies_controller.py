from flask import jsonify

from model.database.Database.Database import Database
from model.recsys.Movie import Movie


def get_all_movies_controller():
    """
    Retrieves all movies from the database and converts them into a list of dictionaries.
    Returns a JSON response containing all the movies and a status code.
    """
    all_movies = []
    movies = Database.db_process(query="SELECT * FROM movies", fetchone=False)
    for movie in movies:
        all_movies.append(Movie.movie_to_dict(movie))
    return jsonify({"allMovies": all_movies}), 200
