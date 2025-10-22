import time
import sqlite3

from data.db.base_db import BaseDB


class FileDB(BaseDB):
    def connect(self) -> None:
        """Подключает базу данных."""
        path = f"{self.path_db}/files.db"
        self._conn = sqlite3.connect(path)
        self._conn.row_factory = sqlite3.Row

        self.logger.debug('db открыта: %s', path)

    def _create_tables(self) -> None:
        """Создает таблицу через (IF NOT EXISTS)."""
        self._conn.execute("""CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT UNIQUE,
            mtime REAL,
            hash TEXT,
            indexed INTEGER DEFAULT 0,
            updated_at REAL
        )""")
        self._conn.commit()

    def get_file_by_path(self, path: str) -> dict | None:
        """Возвращает данные по запросу для последующего сравнения."""
        cur = self._conn.execute("SELECT * FROM files WHERE path = ?", (path,))
        return cur.fetchone()

    def add(self, path: str, mtime: float, hash_: str, indexed: int = 0) -> None:
        """Добавляет запись в базу."""
        self._conn.execute("""
        INSERT INTO files (path, mtime, hash, indexed, updated_at)
        VALUES (?, ?, ?, ?, ?)
        """, (path, mtime, hash_, indexed, time.time()))
        self._conn.commit()

    def update(self, path: str, mtime: float, hash_: str, indexed: int = 0) -> None:
        """Обновляет запись в базе."""
        self._conn.execute("""
        UPDATE files
        SET mtime = ?, hash = ?, indexed = ?, updated_at = ?
        WHERE path = ?
        """, (mtime, hash_, indexed, time.time(), path))
        self._conn.commit()

    def get_unindexed_files(self) -> list[tuple]:
        """Возвращает все файлы которые не были индексированы."""
        cur = self._conn.execute("SELECT * FROM files WHERE indexed = 0")
        return cur.fetchall()
