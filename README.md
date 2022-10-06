# tg_yandex_music_downloader
Проект по мониторингу и ведению каналов с дискографией артистов в телеграм.

## Первый запуск
Установка зависимостей и создание виртуальной среды:
```bash
poetry install
```
Создать `.env` файл с настройкми бота (`.env_example -> .env`):
```bash
TOKEN=<YANDEX AUTH TOKEN>
TG_TOKEN=<TELEGRAM TOKEN>
MAIN_CHAT_ID=<CHAT ID FOR ALBUMS>
BACK_CHAT_ID=<CHAT ID FOR TRACKS>
```

## Запуск
```bash
poetry run python bot.py
```
