import os
import time
import sqlite3

from data.db.base_db import BaseDB


class FileDB(BaseDB):
    def connect(self):
        os.makedirs(self._path_db, exist_ok=True)

        db_path = os.path.join(self._path_db, "files.db")
        self._conn = sqlite3.connect(db_path)
        self._conn.row_factory = sqlite3.Row

        self._create_tables()

    def _create_tables(self):
        self._conn.execute("""CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT UNIQUE,
            mtime REAL,
            hash TEXT,
            indexed INTEGER DEFAULT 0,
            updated_at REAL
        )""")
        self._conn.commit()

    def get_file_by_path(self, path: str):
        cur = self._conn.execute("SELECT * FROM files WHERE path = ?", (path,))
        return cur.fetchone()

    def add(self, path: str, mtime: float, hash_: str, indexed: int = 0):
        self._conn.execute("""
        INSERT INTO files (path, mtime, hash, indexed, updated_at)
        VALUES (?, ?, ?, ?, ?)
        """, (path, mtime, hash_, indexed, time.time()))
        self._conn.commit()

    def update(self, path: str, mtime: float, hash_: str, indexed: int = 0):
        self._conn.execute("""
        UPDATE files
        SET mtime = ?, hash = ?, indexed = ?, updated_at = ?
        WHERE path = ?
        """, (mtime, hash_, indexed, time.time(), path))
        self._conn.commit()

    def get_unindexed_files(self):
        cur = self._conn.execute("SELECT * FROM files WHERE indexed = 0")
        return cur.fetchall()
