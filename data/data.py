import json
from typing import Optional, Dict, List, Union


def get_films(
    file_path: str = "data/data.json", film_id: Optional[int] = None
) -> Union[Dict, List[Dict]]:
    with open(file_path, "r") as f:
        films = json.load(f)["films"]

    if film_id != None and film_id < len(films):
        return films[film_id]

    return films


def add_film(film: dict, file_path="data/data.json") -> None:
    with open(file_path, "r") as f:
        films = json.load(f)
    films["films"].append(film)
    with open(file_path, "w") as f:
        json.dump(films, f, indent=4)
