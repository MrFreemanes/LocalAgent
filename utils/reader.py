import re

from utils.file_io import read_file


def read_file_to_chunks(abs_path: str, chunk_size: int = 1000, overlap: int = 100) -> list[str]:
    """
    Читает текстовый файл по абсолютному пути и возвращает чанки текста.
    """
    text = normalize_text(read_file(abs_path))

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end].strip())
        start += chunk_size - overlap

    return chunks


def normalize_text(_text: str) -> str:
    """
    Получает не обработанный текст.
    Возвращает текст готовый для использования в модели.
    """
    text = _text.replace("\r", " ").replace("\n", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text
