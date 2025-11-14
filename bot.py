import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from commands import (
    FILMS_COMMAND,
    START_COMMAND,
    FILM_CREATE_COMMAND,
    CREATING_EXIT_COMMAND,
    FILMS_BOT_COMMAND,
    START_BOT_COMMAND,
    FILM_CREATE_BOT_COMMAND,
    CREATING_EXIT_BOT_COMMAND,
)
from config import BOT_TOKEN
from data.data import get_films, add_film
from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from models import Film
from validation import is_url_has_image
from keyboards import films_keyboard_markup, FilmCallback

dp = Dispatcher()


class FilmForm(StatesGroup):
    name = State()
    description = State()
    rating = State()
    genre = State()
    actors = State()
    poster = State()


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
    await callback.message.answer_photo(
        caption=text, photo=film.poster, parse_mode="HTML"
    )
    await callback.message.delete()
    await callback.answer()


@dp.message(FILM_CREATE_COMMAND)
async def film_create(message: Message, state: FSMContext):
    await state.set_state(FilmForm.name)
    await message.answer("Введіть назву фільму")


@dp.message(FilmForm.name, F.text)
async def film_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(FilmForm.description)
    await message.answer("Введіть опис фільму")


@dp.message(FilmForm.description, F.text)
async def film_name(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(FilmForm.rating)
    await message.answer(
        "Введіть рейтинг фільму\nРейтинг треба вводити число між 0.00-10.0"
    )


@dp.message(FilmForm.rating, F.text)
async def film_name(message: Message, state: FSMContext):
    await state.update_data(rating=message.text)
    await state.set_state(FilmForm.genre)
    await message.answer("Введіть жанр фільму")


@dp.message(FilmForm.genre, F.text)
async def film_name(message: Message, state: FSMContext):
    await state.update_data(genre=message.text)
    await state.set_state(FilmForm.actors)
    await message.answer(
        "Введіть акторів фільму через кому\nНаприклад Райан Гослінг, Джон Сміт"
    )


@dp.message(FilmForm.actors, F.text)
async def film_name(message: Message, state: FSMContext):
    await state.update_data(actors=message.text)
    await state.set_state(FilmForm.poster)
    await message.answer("Введіть постер фільму")


@dp.message(FilmForm.poster, F.text)
async def film_name(message: Message, state: FSMContext):
    await state.update_data(poster=message.text)

    new_film_data = await state.get_data()
    await state.clear()
    new_film_data["actors"] = list(
        map(lambda x: x.strip(), new_film_data["actors"].split(","))
    )

    try:
        is_url_has_image(new_film_data["poster"])
        new_film = Film(**new_film_data)
        add_film(new_film.model_dump())
        await message.answer("Ви додали фільм")
    except ValueError:
        await message.answer("Помилка в додаванні, спробуйте ще раз")
        await state.set_state(FilmForm.name)
        await message.answer("Введіть назву фільму")


@dp.message(CREATING_EXIT_COMMAND)
async def exit_creating(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Ви успішно покинунли додавання фільму")


async def main():
    bot = Bot(token=BOT_TOKEN)
    await bot.set_my_commands(
        [
            START_BOT_COMMAND,
            FILMS_BOT_COMMAND,
            FILM_CREATE_BOT_COMMAND,
            CREATING_EXIT_BOT_COMMAND,
        ]
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
