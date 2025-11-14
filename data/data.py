import json
from typing import Optional, Dict, List, Union


def get_films(
    file_path: str = "data/data.json", film_id: Optional[int] = None
) -> Union[Dict, List[Dict]]:
    with open(file_path, "r") as f:
        films = json.load(f)["films"]
    for idx, film in enumerate(films):
        film["id"] = idx
    if film_id != None and film_id < len(films):
        return films[film_id]
    return films


def add_film(film: dict, file_path: str = "data/data.json") -> None:
    with open(file_path, "r") as f:
        films = json.load(f)
    films["films"].append(film)
    with open(file_path, "w") as f:
        json.dump(films, f, indent=4)


def search_films(
    query: str, file_path: str = "data/data.json", search_mode: str = "search"
):
    query = query.lower().replace(" ", "")
    with open(file_path, "r") as f:
        films = json.load(f)["films"]
    for idx, film in enumerate(films):
        film["id"] = idx
        film["search_name"] = film["name"].lower().replace(" ", "")
        film["search_genre"] = film["genre"].lower().replace(" ", "")
        film["search_actors"] = "".join(film["actors"]).lower().replace(" ", "")
    return [
        film
        for film in films
        if (query in film["search_name"] and search_mode == "search")
        or (
            query in film["search_genre"] + film["search_actors"]
            and search_mode == "filter"
        )
    ]
