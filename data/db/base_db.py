import logging
from logging import config
from abc import ABC, abstractmethod

from logs.logger_cfg import cfg


class BaseDB(ABC):
    """
    Абстрактный класс для реализации подключения баз данных разной сложности.
    """

    def __init__(self, path_db: str):
        logging.config.dictConfig(cfg)
        self.logger = logging.getLogger('log_db')

        self._path_db = path_db
        self._conn = None
        self.connect()
        self._create_tables()

    def close(self):
        """Закрытие базы."""
        if self._conn:
            self._conn.close()
            self.logger.debug('db закрыта')

    @abstractmethod
    def connect(self):
        """Определение self._conn."""
        pass

    @abstractmethod
    def _create_tables(self) -> None:
        """Создание таблицы если ее нет."""
        pass

    @abstractmethod
    def add(self, *args, **kwargs) -> None:
        """Добавление данных в базу."""
        pass

    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        """Изменение данных в базе."""
        pass
