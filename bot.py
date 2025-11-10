import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from commands import FILMS_COMMAND, START_COMMAND, FILMS_BOT_COMMAND, START_BOT_COMMAND
from config import BOT_TOKEN
from data.data import get_films
from aiogram.types import Message, CallbackQuery
from models import Film
from keyboards import films_keyboard_markup, FilmCallback

dp = Dispatcher()


@dp.message(START_COMMAND)
async def start(message: Message) -> None:
    await message.answer(
        f"Вітаю, {message.from_user.full_name}!\n"
        "Я можу допомогти знайти вам давно забуті улюблені фільми",
    )


@dp.message(FILMS_COMMAND)
async def films(message: Message) -> None:
    data = get_films()
    markup = films_keyboard_markup(data)
    await message.answer("Оберіть фільм:", reply_markup=markup)


@dp.callback_query(FilmCallback.filter())
async def callb_film(callback: CallbackQuery, callback_data: FilmCallback) -> None:
    film_id = callback_data.id
    data = get_films(film_id=film_id)
    film = Film(**data)
    text = (
        f"Фільм: {film.name}\n"
        f"Опис: {film.description}\n"
        f"Рейтинг: {film.rating}\n"
        f"Жанр: {film.genre}\n"
        f"Актори: {', '.join(film.actors)}\n"
    )
    await callback.message.answer_photo(caption=text, photo=film.poster)
    await callback.answer()


async def main():
    bot = Bot(token=BOT_TOKEN)
    await bot.set_my_commands([START_BOT_COMMAND, FILMS_BOT_COMMAND])
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
