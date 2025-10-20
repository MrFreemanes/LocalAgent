"""
В воркере провожу инициализацию баз данных и уже там оперирую ими.
"""

from data.db import files_db, vector_db


def initialize(path_dir_agent: str):
    f_db = files_db.FileDB(path_dir_agent)
    v_db = vector_db.VectorDB(path_dir_agent)

    return f_db, v_db