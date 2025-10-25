import json

import numpy as np
from sentence_transformers import SentenceTransformer

from data.db.vector_db import VectorDB
from utils.reader import normalize_text


class LocalEmbedder:
    """Локальный векторизатор текстов."""

    def __init__(self, model_name: str = "paraphrase-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Преобразует список текстов в список векторов."""
        embeddings = self.model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
        return embeddings.tolist()

    def request(self, query: str, vdb: VectorDB, top_k: int = 5):
        query = normalize_text(query)
        # 1. Вектор запроса
        query_vec = np.array(self.embed([query])[0], dtype=np.float32)
        query_vec /= np.linalg.norm(query_vec)

        # 2. Загружаем все вектора
        results = []
        rows = vdb._conn.execute("SELECT file_path, chunk_index, text, vector FROM vectors").fetchall()
        for row in rows:
            vec = np.array(json.loads(row["vector"]), dtype=np.float32)
            vec /= np.linalg.norm(vec)
            sim = float(np.dot(query_vec, vec))  # косинусное сходство
            results.append({
                "file_path": row["file_path"],
                "chunk_index": row["chunk_index"],
                "text": row["text"],
                "score": sim
            })

        # 3. Сортируем по сходству
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]
