class Movie:
    def __init__(self, title, genres, year, director, actors, plot, poster, imdb_votes, imdb_rating):
        self.title = title
        self.genres = genres
        self.year = year
        self.director = director
        self.actors = actors
        self.plot = plot
        self.poster = poster
        self.imdb_votes = imdb_votes
        self.imdb_rating = imdb_rating

    def to_dict(self):
        return {
            "title": self.title,
            "genres": self.genres,
            "year": self.year,
            "director": self.director,
            "actors": self.actors,
            "plot": self.plot,
            "poster": self.poster,
            "imdb_votes": self.imdb_votes,
            "imdb_rating": self.imdb_rating
        }

    def __str__(self):
        return f"{self.title} ({self.year})"
