import csv
import mysql.connector
from faker import Faker
from datetime import datetime
from mysql_constants import HOST, DBNAME, USERNAME, PASSWORD, INSERT_INTO_USERS_SQL, INSERT_INTO_MOVIES_SQL, \
    INSERT_INTO_LINKS_SQL, INSERT_INTO_RATINGS_SQL


def connect_to_db():
    # Database credentials
    connection = mysql.connector.connect(
        host=HOST,
        user=USERNAME,
        password=PASSWORD,
        database=DBNAME
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
        cursor.execute(INSERT_INTO_USERS_SQL, (i, username, password))

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
    movies_path = "csvdata/movies_metadata.csv"
    links_path = "csvdata/links.csv"
    ratings_path = "csvdata/ratings.csv"

    movies_query = INSERT_INTO_MOVIES_SQL
    links_query = INSERT_INTO_LINKS_SQL
    ratings_query = INSERT_INTO_RATINGS_SQL

    insert_users()
    process_csv(movies_path, movies_query, "movies")
    process_csv(links_path, links_query, "links")
    process_csv(ratings_path, ratings_query, "ratings")
