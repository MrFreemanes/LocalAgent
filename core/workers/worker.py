import multiprocessing as mp

from config.config import Status
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

        task = item['task']
        if task == 'initialize':
            db = initialize(item['new_path'])
        elif task == 'scanning':
            scanning(item['new_path'], db, result_q)


def scanning(new_path: str, files_db, result_q):
    scan = WindowsScanner(new_path, files_db)
    for progress in scan.scan():
        result_q.put({'status': Status.RUN, 'progress': progress})
