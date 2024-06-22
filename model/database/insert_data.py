import csv
import hashlib

import mysql.connector
from faker import Faker
from datetime import datetime

from model.database.Database.Database import Database
from mysql_constants import HOST, DBNAME, USERNAME, PASSWORD, INSERT_INTO_USERS_SQL, INSERT_INTO_MOVIES_SQL, \
    INSERT_INTO_RATINGS_SQL, DELETE_DUPE_RATINGS_SQL, DELETE_DUPE_MOVIES_SQL


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
    username1 = "user1"
    password1 = "user1"
    hashed_password1 = hashlib.sha256(password1.encode()).hexdigest()
    cursor.execute(INSERT_INTO_USERS_SQL, (1, username1, hashed_password1))
    username2 = "user2"
    password2 = "user2"
    hashed_password2 = hashlib.sha256(password2.encode()).hexdigest()
    cursor.execute(INSERT_INTO_USERS_SQL, (2, username2, hashed_password2))

    for i in range(3, num_records + 1):
        username = faker.user_name()
        password = faker.password()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        # Insert fake data into the users table
        cursor.execute(INSERT_INTO_USERS_SQL, (i, username, hashed_password))

    connection.commit()
    connection.close()
    print("Users inserted.")


def decode_string(value):
    try:
        # Attempt to decode using 'latin1' and then re-encode to 'utf-8'
        return value.encode('latin1').decode('utf-8')
    except UnicodeEncodeError:
        # If an error occurs, return the original value
        return value


def process_csv(csv_file, query, type):
    connection = connect_to_db()

    with open(csv_file, newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        cursor = connection.cursor()
        for row in reader:
            # Decode the strings that might have encoding issues
            if type == "movies":
                params = (
                    int(row['id']),
                    decode_string(row['title']),
                    decode_string(row['genre']),
                    row['year'],
                    decode_string(row['director']),
                    decode_string(row['actors']),
                    decode_string(row['plot']),
                    row['poster'],
                    row['imdb_votes'],
                    row['imdb_rating']
                )
            elif type == "ratings":
                params = (
                    int(row['userId']),
                    int(row['movieId']),
                    float(row['rating']),
                    datetime.fromtimestamp(int(row['timestamp']))
                )

            cursor.execute(query, params)

    connection.commit()
    connection.close()
    print("Data inserted successfully!")


if __name__ == "__main__":
    movies_path = "csvdata/movies_metadata.csv"
    ratings_path = "csvdata/ratings.csv"

    movies_query = INSERT_INTO_MOVIES_SQL
    ratings_query = INSERT_INTO_RATINGS_SQL

    insert_users()
    process_csv(movies_path, movies_query, "movies")
    process_csv(ratings_path, ratings_query, "ratings")

    Database.db_process(DELETE_DUPE_RATINGS_SQL, commit_needed=True)
    Database.db_process(DELETE_DUPE_MOVIES_SQL, commit_needed=True)

    print("Done!")
