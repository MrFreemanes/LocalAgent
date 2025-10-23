import time
from utils.reader import read_file_to_chunks


class Vectorizer:
    def __init__(self, files_db, vector_db, model):
        """
        :param files_db: экземпляр FileDB
        :param vector_db: экземпляр VectorDB
        :param model: модель, у которой есть метод .embed(text)
        """
        self.files_db = files_db
        self.vector_db = vector_db
        self.model = model

    def run(self, base_path: str):
        """
        Основной метод — проходит по всем файлам с indexed = 0.
        """
        unindexed_files = self.files_db.get_unindexed_files()
        total = len(unindexed_files)

        if total == 0:
            return

        for i, file in enumerate(unindexed_files, 1):
            try:
                rel_path = file["path"]
                abs_path = f"{base_path}/{rel_path}"

                # 1. Читаем и делим на чанки
                chunks = read_file_to_chunks(abs_path)

                # 2. Векторизация и запись
                for idx, chunk in enumerate(chunks):
                    vector = self.model.embed(chunk)
                    self.vector_db.add_vector(rel_path, idx, chunk, vector)

                # 3. Обновляем статус в FilesDB
                self.files_db.update(
                    path=rel_path,
                    mtime=file["mtime"],
                    hash_=file["hash"],
                    indexed=1
                )

            except Exception as e:
                print(f"[Vectorizer] Ошибка при обработке {file['path']}: {e}")

            yield int(i / total * 100)  # для UI прогресса
