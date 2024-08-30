import json
import random
import pandas as pd
from importlib.resources import files


def load_color(sorted_by_color: bool = True) -> dict:
    """Load available colors material

    Args:
        sorted_by_color (bool, optional): Whether to sort by color. Defaults to True.

    Returns:
        dict: Available colors
    """
    data = (files("material_color.resources")
            .joinpath('material-colors.json')
            .read_text())

    _dict: dict = json.loads(data)

    if sorted_by_color:
        return dict(sorted(_dict.items()))

    return _dict


def generate_random_color() -> str:
    """Generate random color in hex

    Returns:
        str: Random color in hex
    """
    color_json = load_color()
    color_key = random.choice(get_all_colors())
    random_color = random.choice(list(color_json[color_key].keys()))
    return color_json[color_key][random_color]


def get_all_colors() -> list[str]:
    """Get all available named colors

    Returns:
        list[str]: Available colors
    """
    return list(load_color().keys())


def get_color(color_key: str) -> dict[str, str]:
    """Get color by name

    Returns:
        list[str]: Available colors in hex
    """
    assert color_key in get_all_colors(), f"Color must be in {get_all_colors()}"
    return load_color()[color_key]


def get_color_list() -> list[str]:
    """Get hex color as list

    Returns:
        list[str]: Available colors in hex
    """
    colors: list[str] = []
    keys: list[str] = get_all_colors()
    for key in keys:
        for color in get_color(key).values():
            colors.append(color)

    return colors


df: pd.DataFrame = pd.DataFrame(load_color())
