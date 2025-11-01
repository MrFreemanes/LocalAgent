import json, os
import logging
from logging import config
from pathlib import Path

from utils.paths import path_to_config
from logs.logger_cfg import cfg

logging.config.dictConfig(cfg)
logger = logging.getLogger('log_utils')


def save_json(data: dict, path: str = path_to_config('config.json')) -> None:
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as err:
        logger.error('Ошибка сохранения файла %s: %s', path, err)


def load_json(path: str = path_to_config('config.json')) -> dict | None:
    if not os.path.isfile(path):
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as err:
        logger.error('Ошибка загрузки файла %s: %s', path, err)


def read_file(path: str) -> str | None:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Файл {file_path} не найден")

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()
