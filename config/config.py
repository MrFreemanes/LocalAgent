from dataclasses import dataclass


class Status:
    """Используется в Bridge и в worker"""
    RUN = 'run'
    DONE = 'done'
    ERROR = 'error'


@dataclass(repr=True)
class Task:
    task: str
    new_path: str = None


@dataclass(repr=True)
class Result:
    data: dict
    status: str
    progress: int
    text_error: str = 'Ошибка'
