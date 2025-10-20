"""
В воркере провожу инициализацию баз данных и уже там оперирую ими.
"""
import os

from data.db import files_db, vector_db


def initialize(path_dir_agent: str):
    dir_agent = f"{path_dir_agent}/LocalAgent"
    os.makedirs(dir_agent, exist_ok=True)

    f_db = files_db.FileDB(dir_agent)

    return f_db
