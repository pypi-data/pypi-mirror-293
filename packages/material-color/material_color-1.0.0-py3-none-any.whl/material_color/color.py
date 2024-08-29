import json
import random
import pandas as pd
from importlib.resources import files


def load_color(sorted_by_color: bool = True) -> dict:
    data = (files("material_color.resources")
            .joinpath('material-colors.json')
            .read_text())

    _dict: dict = json.loads(data)

    if sorted_by_color:
        return dict(sorted(_dict.items()))

    return _dict


def generate_random_color() -> str:
    color_json = load_color()
    color_key = random.choice(get_all_colors())
    random_color = random.choice(list(color_json[color_key].keys()))
    return color_json[color_key][random_color]


def get_all_colors() -> list[str]:
    return list(load_color().keys())


def get_color(color_key: str) -> list[str]:
    assert color_key in get_all_colors(), f"Color must be in {get_all_colors()}"
    return load_color()[color_key]


df: pd.DataFrame = pd.DataFrame(load_color())
