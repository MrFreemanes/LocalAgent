import sqlite3
import time
import json

from data.db.base_db import BaseDB


class VectorDB(BaseDB):
    """
    База данных для хранения векторов и связанных с ними текстовых чанков.
    """

    def connect(self):
        self._conn = sqlite3.connect(f"{self.path_db}/vectors.db")
        self._conn.row_factory = sqlite3.Row

    def _create_tables(self):
        self._conn.execute("""
        CREATE TABLE IF NOT EXISTS vectors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT,
            chunk_index INTEGER,
            text TEXT,
            vector TEXT,
            created_at REAL
        )
        """)
        self._conn.commit()

    def add(self, file_path: str, chunk_index: int, text: str, vector: list[float]) -> None:
        """Добавление нового вектора."""
        try:
            self._conn.execute("""
            INSERT INTO vectors (file_path, chunk_index, text, vector, created_at)
            VALUES (?, ?, ?, ?, ?)
            """, (file_path, chunk_index, text, json.dumps(vector), time.time()))
            self._conn.commit()
            self.logger.debug('[VectorDB] Добавлен вектор %s #%s', file_path, chunk_index)
        except Exception as e:
            self.logger.error('[VectorDB] Ошибка при добавлении: %s', e)

    def update(self, file_path: str, chunk_index: int, text: str, vector: list[float]) -> None:
        """Обновление существующего вектора (по пути и индексу чанка)."""
        try:
            self._conn.execute("""
            UPDATE vectors 
            SET text = ?, vector = ?, created_at = ?
            WHERE file_path = ? AND chunk_index = ?
            """, (text, json.dumps(vector), time.time(), file_path, chunk_index))
            self._conn.commit()
            self.logger.debug('[VectorDB] Обновлён вектор ^s #%s', file_path, chunk_index)
        except Exception as e:
            self.logger.error('[VectorDB] Ошибка при обновлении: %s', e)

    def get_vectors_by_file(self, file_path: str):
        """Возвращает все векторы по конкретному файлу."""
        cur = self._conn.execute("""
        SELECT * FROM vectors WHERE file_path = ?
        """, (file_path,))
        return cur.fetchall()

    def delete_vectors_by_file(self, file_path: str):
        """Удаляет все векторы, связанные с файлом."""
        self._conn.execute("""
        DELETE FROM vectors WHERE file_path = ?
        """, (file_path,))
        self._conn.commit()
        self.logger.debug('[VectorDB] Удалены векторы для %s', file_path)
