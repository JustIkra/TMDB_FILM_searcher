import sqlite3

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS excluded_movies (
        user_id INTEGER,
        movie_title TEXT
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS last_movie (
        user_id INTEGER PRIMARY KEY,
        movie_id INTEGER,
        title TEXT,
        original_title TEXT,
        poster_url TEXT,
        overview TEXT,
        genres TEXT
    )""")
    conn.commit()

def load_excluded_movies(user_id):
    cursor.execute("SELECT movie_title FROM excluded_movies WHERE user_id = ?", (user_id,))
    return [row[0] for row in cursor.fetchall()]

def add_excluded_movie(user_id, movie_title):
    cursor.execute("INSERT INTO excluded_movies (user_id, movie_title) VALUES (?, ?)", (user_id, movie_title))
    conn.commit()

def remove_excluded_movie(user_id, movie_title):
    cursor.execute("DELETE FROM excluded_movies WHERE user_id = ? AND movie_title = ?", (user_id, movie_title))
    conn.commit()

def save_last_movie(user_id, movie):
    cursor.execute("""
    INSERT OR REPLACE INTO last_movie (user_id, movie_id, title, original_title, poster_url, overview, genres) 
    VALUES (?, ?, ?, ?, ?, ?, ?)""", 
    (user_id, movie['movie_id'], movie['title'], movie['original_title'], movie['poster_url'], movie['overview'], movie['genres']))
    conn.commit()

def get_last_movie(user_id):
    cursor.execute("SELECT movie_id, title, original_title, poster_url, overview, genres FROM last_movie WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()
    if data:
        return {
            "movie_id": data[0],
            "title": data[1],
            "original_title": data[2],
            "poster_url": data[3],
            "overview": data[4],
            "genres": data[5]
        }
    return None

init_db()
