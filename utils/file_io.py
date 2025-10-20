import json, os

from utils.paths import path_to_config


def save_json(data: dict, path: str = path_to_config('config.json')) -> None:
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as err:
        # TODO: logging
        pass


def load_json(path: str = path_to_config('config.json')) -> dict | None:
    if not os.path.isfile(path):
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as err:
        # TODO: logging
        pass
