from pathlib import Path
import re


def read_file_to_chunks(abs_path: str, chunk_size: int = 1000, overlap: int = 100) -> list[str]:
    """
    Читает текстовый файл по абсолютному пути и возвращает чанки текста.
    """
    file_path = Path(abs_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Файл {file_path} не найден")

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    text = text.replace("\r", " ").replace("\n", " ")
    text = re.sub(r"\s+", " ", text).strip()

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end].strip())
        start += chunk_size - overlap

    return chunks
