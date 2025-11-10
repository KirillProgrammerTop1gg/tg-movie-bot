import json
from typing import Optional, Dict, List, Union


def get_films(
    file_path: str = "data/data.json", film_id: Optional[int] = None
) -> Union[Dict, List[Dict]]:
    with open(file_path, "r") as f:
        films = json.loads(f.read())["films"]

    if film_id != None and film_id < len(films):
        return films[film_id]

    return films
