# TMDB Film Searcher Bot

## Описание

Этот бот для Telegram помогает искать фильмы по описанию, используя [TMDB API](https://www.themoviedb.org/) и GPT-4o.
Пользователь может описать фильм, который хочет посмотреть, а бот предложит подходящий вариант и даст краткую информацию о нем.
Фильмы можно добавлять в список исключений — они не будут предлагаться снова.

---

## Возможности

* Поиск фильмов по описанию на естественном языке.
* Исключение нежелательных фильмов из выдачи.
* Сохранение информации о последнем предложенном фильме.
* Хранение списка исключённых фильмов для каждого пользователя.
* Интеграция с GPT-4o для интерпретации пользовательских описаний.
* Использование переменных окружения из `.env` для хранения ключей.

---

## Установка

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/your_username/TMDB_film_searcher.git
   cd TMDB_film_searcher
   ```

2. **Создайте виртуальное окружение (по желанию):**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. **Установите зависимости:**

   ```bash
   pip install -r requirements.txt
   ```

---

## Настройка переменных окружения

1. **Создайте файл `.env` в корне проекта**
   (можете скопировать и переименовать пример):

   ```
   cp .env.example .env
   ```
2. **Добавьте в `.env` свои ключи:**

   ```
   TG_TOKEN=your_telegram_bot_token
   TMDB_API_KEY=your_tmdb_api_key
   ```

* Получить токен для Telegram-бота можно через [BotFather](https://core.telegram.org/bots#botfather).
* Ключ TMDB получите на [TMDB Developers](https://developers.themoviedb.org/3/getting-started/introduction).

---

## Запуск

**Из корня проекта**:

```bash
python -m src.bot
```

---

## Структура проекта

```
TMDB_film_searcher/
├── src/
│   ├── bot.py
│   ├── config.py
│   ├── db.py
│   ├── tmdb.py
│   └── gpt_helper.py
├── .env.example
├── requirements.txt
├── README.md
├── users.db
└── .gitignore
```

---

## Использование

* При первом запуске напишите `/start` боту в Telegram.
* Опишите фильм, который вы хотите посмотреть — бот предложит название и описание.
* Для любого предложенного фильма можно нажать кнопку «Добавить в исключения», чтобы он больше не предлагался.
* Список исключённых фильмов доступен по команде `/show_exclusions`.
* Для удаления фильма из исключений используйте `/remove_exclusion название_фильма`.

---

## Зависимости

* [pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/)
* [requests](https://pypi.org/project/requests/)
* [g4f](https://pypi.org/project/g4f/)
* [python-dotenv](https://pypi.org/project/python-dotenv/)

---
