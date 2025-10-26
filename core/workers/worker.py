import multiprocessing as mp
import logging
from logging import config

from config.config import Status, Result
from utils.agent_init import initialize
from core.scanning.windows_scan import WindowsScanner
from core.vectorizers.vectorizer import Vectorizer
from logs.logger_cfg import cfg

logging.config.dictConfig(cfg)
logger = logging.getLogger('log_worker')


def worker(task_q: mp.Queue, result_q: mp.Queue):
    """
    CPU-GPU-IO нагрузка. Используется как отдельный процесс.
    :param task_q: Очередь с задачами
    :param result_q: Очередь с результатами
    """
    f_db, v_db, model = None, None, None
    while True:
        item = task_q.get()

        if item is None: break

        logger.debug('Получена задача %s', item.__repr__())
        task = item.task
        path = item.new_path

        if task == 'init':
            logger.debug('initialize путь: %s', path)
            if f_db is not None and v_db is not None:
                f_db.close()
                v_db.close()
            f_db, v_db, model = initialize(path, result_q)
        elif task == 'scanning' and f_db is not None:
            logger.debug('scanning путь: %s', path)
            scanning(path, f_db, result_q)
        elif task == 'vector':
            logger.debug('vector путь: %s', path)
            vectorization(path, f_db, v_db, model, result_q)
        elif task == 'request' and model is not None and item.query is not None:
            logger.debug('request текст: %s', item.query)
            results = model.request(item.query, v_db)
            result_q.put(Result({'worker': 'request', 'data': results}, Status.DONE, 100))

    if f_db is not None and v_db is not None:
        f_db.close()
        v_db.close()


def scanning(path: str, files_db, result_q) -> None:
    """
    Запускает сканирование в указанной папке.
    Передает прогресс в Bridge.
    :param path: Путь до папки для сканирования.
    :param files_db: Экземпляр класса FileDB.
    :param result_q: Очередь для отправки результатов.
    """
    scan = WindowsScanner(path, files_db)
    for progress in scan.scan():
        if 100 > progress > 0:
            result_q.put(Result({'worker': 'scanning'}, Status.RUN, progress))
        elif progress == 100:
            result_q.put(Result({'worker': 'scanning'}, Status.DONE, 100))
        else:
            result_q.put(Result({'worker': 'scanning'}, Status.ERROR, 100,
                                text_error='Ошибка: директория не была просканирована'))
            logger.warning('Ошибка: директория не была просканирована')


def vectorization(path: str, files_db, vector_db, model, result_q) -> None:
    """
    Функция для векторизации.
    :param model: Созданная в initialize() модель
    :param path: Путь до папки для векторизации.
    :param files_db: Класс взаимодействия с files.db.
    :param vector_db: Класс взаимодействия с vectors.db.
    :param result_q: Очередь для отправки результатов.
    """

    vectorizer = Vectorizer(files_db, vector_db, model, path)
    for progress in vectorizer.run():
        if 100 > progress > 0:
            result_q.put(Result({'worker': 'vector'}, Status.RUN, progress, ))
        elif progress == 100:
            result_q.put(Result({'worker': 'vector'}, Status.DONE, 100, ))
        elif progress == 0:
            result_q.put(Result({'worker': 'vector'}, Status.DONE, 100, ))
        else:
            logger.warning('Ошибка, progress = %s', progress)
