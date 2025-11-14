from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from typing import List, Dict


class FilmCallback(CallbackData, prefix="film", sep=";"):
    id: int
    name: str


def films_keyboard_markup(film_list: List[Dict]):
    builder = InlineKeyboardBuilder()
    builder.adjust(1, repeat=True)

    for index, film in enumerate(film_list):
        callback_data = FilmCallback(id=film["id"], name=film["name"])
        builder.button(text=film["name"], callback_data=callback_data.pack())

    return builder.as_markup()


class SearchCallback(CallbackData, prefix="search", sep=";"):
    s: str


def search_keyboard_markup():
    builder = InlineKeyboardBuilder()
    builder.adjust(1, repeat=True)

    builder.button(text="назвою", callback_data=SearchCallback(s="search"))
    builder.button(text="актором чи жанром", callback_data=SearchCallback(s="filter"))

    return builder.as_markup()
