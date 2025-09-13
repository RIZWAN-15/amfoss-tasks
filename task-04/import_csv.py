import mysql.connector

# Connect to the database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rizzu",
    database="cinescope"
)
cursor = conn.cursor(dictionary=True)

# Get all column names dynamically
cursor.execute("SHOW COLUMNS FROM movies")
columns_info = cursor.fetchall()
columns = [col['Field'].lower() for col in columns_info]  # make lowercase for safety

# Identify the important columns dynamically
def find_column(possible_names):
    for name in possible_names:
        if name.lower() in columns:
            return name
    return None

title_col = find_column(['Series_Title', 'series_title', 'title'])
year_col = find_column(['Released_Year', 'released_year', 'year'])
rating_col = find_column(['IMDB_Rating', 'imdb_rating', 'rating'])
director_col = find_column(['Director', 'director', 'filmmaker'])

if not all([title_col, year_col, rating_col, director_col]):
    print("Error: Could not find one or more required columns in the database.")
    cursor.close()
    conn.close()
    exit()

# Get director name from user
director_name = input("Enter director name: ")

# Build and execute query dynamically
query = f"""
    SELECT {title_col}, {year_col}, {rating_col} 
    FROM movies
    WHERE LOWER({director_col}) LIKE LOWER(%s)
"""
cursor.execute(query, (f"%{director_name}%",))
results = cursor.fetchall()

# Print results
if results:
    for row in results:
        print(f"{row[title_col]} ({row[year_col]}) ⭐ {row[rating_col]}")
else:
    print("No movies found.")

cursor.close()
conn.close()

