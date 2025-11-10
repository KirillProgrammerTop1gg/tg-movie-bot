from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand

START_COMMAND = Command("start")
FILMS_COMMAND = Command("films")

START_BOT_COMMAND = BotCommand(command="start", description="Почати розмову")
FILMS_BOT_COMMAND = BotCommand(command="films", description="Перегляд списку фільмів")
