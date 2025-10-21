import logging
from logging import config
from abc import ABC, abstractmethod

from logs.logger_cfg import cfg


class BaseScanner(ABC):
    def __init__(self, vault_path: str, db):
        logging.config.dictConfig(cfg)
        self.logger = logging.getLogger('log_scan')

        self._vault_path = vault_path
        self._db = db

    @abstractmethod
    def scan(self):
        pass
