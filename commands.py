from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand

START_COMMAND = Command("start")
FILMS_COMMAND = Command("films")
FILM_CREATE_COMMAND = Command("create_film")
CREATING_EXIT_COMMAND = Command("creating_exit")

START_BOT_COMMAND = BotCommand(command="start", description="Почати розмову")
FILMS_BOT_COMMAND = BotCommand(command="films", description="Перегляд списку фільмів")
FILM_CREATE_BOT_COMMAND = BotCommand(
    command="create_film", description="Додати фільм у базу"
)
CREATING_EXIT_BOT_COMMAND = BotCommand(
    command="creating_exit", description="Зупинити додавання фільма"
)
