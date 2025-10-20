from abc import ABC, abstractmethod


class BaseDB(ABC):
    def __init__(self, path_db: str):
        self._path_db = path_db
        self._conn = None
        self.connect()

    def close(self):
        if self._conn:
            self._conn.close()

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def _create_tables(self) -> None:
        pass

    @abstractmethod
    def add(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        pass
