import os
import logging
from logging import config
from multiprocessing import Queue

from data.db import files_db, vector_db
from config.config import Result, Status
from logs.logger_cfg import cfg

logging.config.dictConfig(cfg)
logger = logging.getLogger('log_utils')


def initialize(path_dir_agent: str, result_q: Queue) -> files_db.FileDB | None:
    """
    Проверяет наличие переданной папки.
    Возвращает классы: FileDB (подключенные базы данных)
    """
    if os.path.exists(path_dir_agent):
        dir_agent = f"{path_dir_agent}/LocalAgent"
        os.makedirs(dir_agent, exist_ok=True)

        f_db = files_db.FileDB(dir_agent)

        logger.debug('Базы данных успешно инициализированы')

        return f_db
    else:
        # отключать интерфейс при этой ошибке чтобы пользователь не смог сканировать не существующую папку.
        result_q.put(Result({}, Status.ERROR, 100, text_error=f"Директории {path_dir_agent} не существует"))
        logger.warning('Директории %s не существует', path_dir_agent)
        return None
