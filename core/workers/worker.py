import multiprocessing as mp

from config.config import Status, Result
from utils.agent_init import initialize
from core.scanning.windows_scan import WindowsScanner


def worker(task_q: mp.Queue, result_q: mp.Queue):
    """
    CPU-GPU-IO нагрузка. Используется как отдельный процесс.
    :param task_q: Очередь с задачами
    :param result_q: Очередь с результатами
    """
    db = initialize(r'C:\Users\notebook\Desktop\test_LocalAgent')
    while True:
        item = task_q.get()

        if item is None: break

        task = item.task

        if task == 'initialize':
            db.close()
            db = initialize(item.new_path)
        elif task == 'scanning':
            scanning(r'C:\Users\notebook\Desktop\test_LocalAgent', db, result_q)


def scanning(path: str, files_db, result_q) -> None:
    """
    Запускает сканирование в указанной папке.
    :param path: Название папки для сканирования.
    :param files_db: Экземпляр класса FileDB.
    :param result_q: Очередь для отправки результатов.
    """
    scan = WindowsScanner(path, files_db)
    for progress in scan.scan():
        result_q.put(Result({}, Status.RUN, progress))

