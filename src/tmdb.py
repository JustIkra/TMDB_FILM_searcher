import requests
from config import TMDB_API_KEY

TMDB_GENRES = {
    28: "Боевик", 12: "Приключения", 16: "Анимация", 35: "Комедия",
    80: "Криминал", 99: "Документальный", 18: "Драма", 10751: "Семейный",
    14: "Фэнтези", 36: "История", 27: "Ужасы", 10402: "Музыка",
    9648: "Мистика", 10749: "Мелодрама", 878: "Научная фантастика",
    53: "Триллер", 10752: "Военный", 37: "Вестерн"
}

def search_tmdb(query):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}&language=ru-RU"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            return data['results'][0]
    return None

def get_movie_info(movie):
    title = movie.get('title') or movie.get('name')
    original_title = movie.get('original_title') or movie.get('title')
    overview = movie.get('overview') or "Нет обзора"
    genre_ids = movie.get('genre_ids', [])
    genres = ', '.join([TMDB_GENRES.get(genre_id, "Неизвестный жанр") for genre_id in genre_ids])
    adult = movie.get('adult', False)
    age_rating = "18+" if adult else "Для всех"
    poster_url = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get('poster_path') else None
    link = f"https://www.themoviedb.org/movie/{movie.get('id')}" if 'id' in movie else None
    return {
        "title": title,
        "original_title": original_title,
        "overview": overview,
        "genres": genres,
        "age_rating": age_rating,
        "poster_url": poster_url,
        "link": link,
        "movie_id": movie.get('id')
    }
