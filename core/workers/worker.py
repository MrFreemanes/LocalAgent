import multiprocessing as mp
import logging
from logging import config

from config.config import Status, Result
from utils.agent_init import initialize
from core.scanning.windows_scan import WindowsScanner
from logs.logger_cfg import cfg

logging.config.dictConfig(cfg)
logger = logging.getLogger()


def worker(task_q: mp.Queue, result_q: mp.Queue):
    """
    CPU-GPU-IO нагрузка. Используется как отдельный процесс.
    :param task_q: Очередь с задачами
    :param result_q: Очередь с результатами
    """
    db = initialize(r'C:\Users\notebook\Desktop\test_LocalAgent')  # TODO: Загрузка последней открытой папки пир запуске
    while True:
        item = task_q.get()

        if item is None: break

        logger.debug('Получена задача %s', item.__repr__())
        task = item.task

        if task == 'initialize':
            path = item.new_path
            logger.debug('initialize путь: %s', path)

            db.close()
            db = initialize(path)
        elif task == 'scanning':
            logger.debug('scanning', r'C:\Users\notebook\Desktop\test_LocalAgent')
            scanning(r'C:\Users\notebook\Desktop\test_LocalAgent', db, result_q)

    db.close()

def scanning(path: str, files_db, result_q) -> None:
    """
    Запускает сканирование в указанной папке.
    Передает прогресс в Bridge.
    :param path: Название папки для сканирования.
    :param files_db: Экземпляр класса FileDB.
    :param result_q: Очередь для отправки результатов.
    """
    scan = WindowsScanner(path, files_db)
    for progress in scan.scan():
        result_q.put(Result({}, Status.RUN, progress))
    result_q.put(Result({}, Status.DONE, 100))
