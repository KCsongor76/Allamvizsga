import mysql.connector
from mysql_constants import HOST, USERNAME, PASSWORD, DBNAME, CREATE_DB_SQL, CREATE_TABLES_SQL

# Create a new connection
conn = mysql.connector.connect(
    host=HOST,
    user=USERNAME,
    password=PASSWORD
)

# Check the connection
if conn.is_connected():
    print("Connected to MySQL")

# Create a cursor object
cursor = conn.cursor()

# Create the database
try:
    cursor.execute(CREATE_DB_SQL)
    print("Database created successfully")
except mysql.connector.Error as err:
    print(f"Error creating database: {err}")

# Close cursor and connection to create a new one to the created database
cursor.close()
conn.close()

# Create a new connection to the created database
conn = mysql.connector.connect(
    host=HOST,
    user=USERNAME,
    password=PASSWORD,
    database=DBNAME
)

# Check the connection
if conn.is_connected():
    print("Connected to MySQL")

# Create a cursor object
cursor = conn.cursor()

# Execute the SQL queries
try:
    cursor.execute(CREATE_TABLES_SQL, multi=True)
    print("Tables created successfully")
except mysql.connector.Error as err:
    print(f"Error creating tables: {err}")

# Close cursor and connection
cursor.close()
conn.close()
