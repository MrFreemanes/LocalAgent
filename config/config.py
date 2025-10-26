from dataclasses import dataclass


class Status:
    """Используется в Bridge и в worker"""
    RUN = 'run'
    DONE = 'done'
    ERROR = 'error'


@dataclass(repr=True)
class Task:
    """
    Датакласс для передачи задач в worker.
    :new_path: Путь дли инициализации папки.
    :query: Текст запроса пользователя для модели.
    """
    task: str
    new_path: str = None
    query: str = None


@dataclass(repr=True)
class Result:
    """
    Датакласс для передачи результата включая ошибки.
    :status: Status.
    """
    data: dict
    status: str
    progress: int
    text_error: str = 'Ошибка'
