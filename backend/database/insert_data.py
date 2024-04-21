import csv
import mysql.connector
from faker import Faker
from datetime import datetime


def connect_to_db():
    # Database credentials
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='movielens_db'
    )
    return connection


def insert_users():
    connection = connect_to_db()
    faker = Faker()

    num_records = 610

    cursor = connection.cursor()
    for i in range(1, num_records + 1):
        username = faker.user_name()
        password = faker.password()

        # Insert fake data into the users table
        sql = "INSERT INTO users (userId, username, password) VALUES (%s, %s, %s)"
        cursor.execute(sql, (i, username, password))

    connection.commit()
    connection.close()
    print("Users inserted.")


def process_csv(csv_file, query, type):
    connection = connect_to_db()

    with open(csv_file, newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        cursor = connection.cursor()
        for row in reader:
            # print(row)
            if type == "movies":
                params = (int(row['id']), row['title'], row['genre'], row['year'], row['director'], row['actors'],
                          row['plot'], row['poster'], row['imdb_votes'], row['imdb_rating'])
            elif type == "links":
                params = (int(row['movieId']), row['imdbId'], row['tmdbId'])
            elif type == "ratings":
                params = (int(row['userId']), int(row['movieId']), float(row['rating']),
                          datetime.fromtimestamp(int(row['timestamp'])))

            cursor.execute(query, params)

    connection.commit()
    connection.close()
    print("Data inserted successfully!")


if __name__ == "__main__":
    movies_path = "movies_metadata.csv"
    links_path = "links.csv"
    ratings_path = "ratings.csv"

    movies_query = ("INSERT INTO movies"
                    " (movieId, title, genre, year, director, actors, plot, poster, imdb_votes, imdb_rating)"
                    " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    links_query = "INSERT INTO links (movieId, imdbId, tmdbId) VALUES (%s, %s, %s)"
    ratings_query = "INSERT INTO ratings (userId, movieId, rating, timestamp) VALUES (%s, %s, %s, %s)"

    insert_users()
    process_csv(movies_path, movies_query, "movies")
    process_csv(links_path, links_query, "links")
    process_csv(ratings_path, ratings_query, "ratings")
