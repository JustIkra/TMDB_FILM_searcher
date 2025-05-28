from g4f.client import Client

client = Client()

def process_user_request(user_request, user_id, load_excluded_movies_func):
    excluded_movies = load_excluded_movies_func(user_id)
    exclusions_text = ", ".join(f"'{movie}'" for movie in excluded_movies)
    prompt = (f"Преобразуй следующее описание в название реально существующего фильма, ответом должно стать его оригинальное название,Исключая фильмы записанные в 'Исключение'. "
              f"Исключение: {exclusions_text}. "
              f"Описание: {user_request}")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()
