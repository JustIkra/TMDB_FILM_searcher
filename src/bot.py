import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import TOKEN
from db import (
    load_excluded_movies, add_excluded_movie, remove_excluded_movie, 
    save_last_movie, get_last_movie
)
from tmdb import search_tmdb, get_movie_info
from gpt_helper import process_user_request

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id, 
        "Привет! Опишите фильм, который хотите посмотреть.\n\n"
        "Команды:\n"
        "/show_exclusions - Показать список исключений\n"
        "/remove_exclusion название - Удалить фильм из исключений"
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('add_exclusion:'))
def callback_add_exclusion(call):
    user_id = call.message.chat.id
    original_title = call.data.split(":", 1)[1].strip()
    excluded_movies = load_excluded_movies(user_id)
    if original_title in excluded_movies:
        bot.answer_callback_query(call.id, text=f"Фильм '{original_title}' уже в списке исключений.", show_alert=True)
    else:
        add_excluded_movie(user_id, original_title)
        bot.answer_callback_query(call.id, text=f"Фильм '{original_title}' добавлен в исключения.", show_alert=True)

@bot.message_handler(commands=['show_exclusions'])
def show_exclusions(message):
    excluded_movies = load_excluded_movies(message.chat.id)
    if excluded_movies:
        excluded_list = "\n".join(excluded_movies)
        bot.send_message(message.chat.id, f"Список исключенных фильмов:\n{excluded_list}")
    else:
        bot.send_message(message.chat.id, "Список исключенных фильмов пуст.")

@bot.message_handler(commands=['remove_exclusion'])
def remove_exclusion(message):
    user_id = message.chat.id
    movie_title = message.text.replace("/remove_exclusion", "").strip()
    excluded_movies = load_excluded_movies(user_id)
    if movie_title in excluded_movies:
        remove_excluded_movie(user_id, movie_title)
        bot.send_message(user_id, f"Фильм '{movie_title}' удален из списка исключений.")
    else:
        bot.send_message(user_id, f"Фильм '{movie_title}' не найден в списке исключений.")

def send_movie_info(chat_id, movie):
    info = get_movie_info(movie)
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text="Добавить в исключения",
            callback_data=f"add_exclusion:{info['original_title']}"
        )
    )
    bot.send_photo(
        chat_id, info["poster_url"] or "", caption=
        f"🎥 <b>{info['title']}</b>\n"
        f"📌 <b>Жанры:</b> {info['genres']}\n"
        f"📆 <b>Возрастное ограничение:</b> {info['age_rating']}\n"
        f"🔗 <a href='{info['link']}'>Смотреть</a>\n\n"
        f"📝 <b>Обзор:</b> {info['overview']}",
        parse_mode='HTML', reply_markup=markup
    )
    save_last_movie(chat_id, info)

@bot.message_handler(content_types=['text'])
def text(message):
    user_request = message.text
    query = process_user_request(user_request, message.chat.id, load_excluded_movies)
    movie = search_tmdb(query)
    if movie:
        send_movie_info(message.chat.id, movie)
    else:
        bot.send_message(message.chat.id, "Не удалось найти подходящий фильм.")

if __name__ == "__main__":
    bot.polling()
