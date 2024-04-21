import mysql.connector

# Database credentials
host = "localhost"
username = "root"
password = ""
dbname = "movielens_db"

# Create a new connection
conn = mysql.connector.connect(
    host=host,
    user=username,
    password=password
)

# Check the connection
if conn.is_connected():
    print("Connected to MySQL")

# Create a cursor object
cursor = conn.cursor()

# Create the database
try:
    cursor.execute(f"CREATE DATABASE {dbname}")
    print("Database created successfully")
except mysql.connector.Error as err:
    print(f"Error creating database: {err}")

# Close cursor and connection to create a new one to the created database
cursor.close()
conn.close()

# Create a new connection to the created database
conn = mysql.connector.connect(
    host=host,
    user=username,
    password=password,
    database=dbname
)

# Check the connection
if conn.is_connected():
    print("Connected to MySQL")

# Create a cursor object
cursor = conn.cursor()

# SQL queries to create the tables
sql = """
    CREATE TABLE users (
        userId INT(11) PRIMARY KEY, 
        username VARCHAR(255),
        password VARCHAR(255)
    );
    CREATE TABLE movies (
        movieId INT(11) PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        genre VARCHAR(255) NOT NULL,
        year VARCHAR(255) NOT NULL,
        director VARCHAR(255) NOT NULL,
        actors VARCHAR(255) NOT NULL,
        plot VARCHAR(255) NOT NULL,
        poster VARCHAR(255) NOT NULL,
        imdb_votes VARCHAR(255) NOT NULL,
        imdb_rating VARCHAR(255) NOT NULL
    );
    CREATE TABLE links (
        movieId INT(11),
        imdbId VARCHAR(11),
        tmdbId VARCHAR(11),
        PRIMARY KEY (movieId),
        FOREIGN KEY (movieId) REFERENCES movies(movieId)
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

# Execute the SQL queries
try:
    cursor.execute(sql, multi=True)
    print("Tables created successfully")
except mysql.connector.Error as err:
    print(f"Error creating tables: {err}")

# Close cursor and connection
cursor.close()
conn.close()
