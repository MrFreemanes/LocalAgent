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
            vectorization(path, f_db, v_db, model, result_q)

    if f_db is not None and v_db is not None:
        f_db.close()
        v_db.close()


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
        if 100 > progress > 0:
            result_q.put(Result({}, Status.RUN, progress))
        elif progress == 100:
            result_q.put(Result({}, Status.DONE, 100))
        else:
            result_q.put(Result({}, Status.ERROR, 100, text_error='Ошибка: директория не была просканирована'))


def vectorization(path: str, files_db, vector_db, model, result_q) -> None:
    """

    :param path:
    :param files_db:
    :param vector_db:
    :param result_q:
    """

    vectorizer = Vectorizer(files_db, vector_db, model, path)
    for progress in vectorizer.run():
        print(progress)
