from sentence_transformers import SentenceTransformer


class LocalEmbedder:
    """Локальный векторизатор текстов."""

    def __init__(self, model_name: str = "paraphrase-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Преобразует список текстов в список векторов."""
        embeddings = self.model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
        return embeddings.tolist()
