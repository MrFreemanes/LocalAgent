from abc import ABC, abstractmethod


class BaseScanner(ABC):
    def __init__(self, vault_path: str, db):
        self._vault_path = vault_path
        self._db = db

    @abstractmethod
    def scan(self):
        pass
