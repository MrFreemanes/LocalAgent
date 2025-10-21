import os
from multiprocessing import Queue

from data.db import files_db, vector_db
from config.config import Result, Status


def initialize(path_dir_agent: str, result_q: Queue) -> files_db.FileDB | None:
    if os.path.exists(path_dir_agent):
        dir_agent = f"{path_dir_agent}/LocalAgent"
        os.makedirs(dir_agent, exist_ok=True)

        f_db = files_db.FileDB(dir_agent)

        return f_db
    else:
        result_q.put(Result({}, Status.ERROR, 100, text_error=f"Директории {path_dir_agent} не существует"))
        return None
