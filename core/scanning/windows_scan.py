from pathlib import Path

from core.scanning.base_scan import BaseScanner
from utils.hashing import hash_file


class WindowsScanner(BaseScanner):
    def scan(self):
        """Сканирует все файлы в папке и подпапках."""
        vault = Path(self._vault_path)
        if not vault.exists():
            yield 0
            self.logger.debug('Не существует директории по указанному пути: %s', self._vault_path)
            return

        files = self._collect_files(vault)
        total = len(files)
        if total == 0:
            yield 100
            self.logger.debug('В папке не найдены файлы')
            return

        last_progress = -1
        i = 0
        for i, file in enumerate(files, 1):
            self._process_file(vault, file)
            progress = int(i / total * 100)
            if progress >= last_progress + 1 or progress == 100:
                yield progress
                last_progress = progress

        self.logger.debug('Просканировано %s файлов в %s', i, self._vault_path)

    def _collect_files(self, vault: Path) -> list[Path]:
        """Собирает все файлы, игнорируя служебные директории."""
        ignore_dirs = {"LocalAgent"}

        files = []
        for f in vault.rglob("*.*"):
            if not f.is_file():
                continue

            # Пропускаем файлы внутри служебных директорий
            if any(ignored in f.parts for ignored in ignore_dirs):
                continue

            files.append(f)

        return files

    def _process_file(self, vault: Path, file: Path) -> None:
        """Обрабатывает один файл — проверяет хэш и обновляет БД."""
        rel_path = file.relative_to(vault)
        try:
            mtime = file.stat().st_mtime
            hash_ = hash_file(file)
            existing = self._db.get_file_by_path(str(rel_path))

            if not existing:
                self._db.add(str(rel_path), mtime, hash_)
            elif existing["hash"] != hash_:
                self._db.update(str(rel_path), mtime, hash_, indexed=0)
        except Exception as e:
            self.logger.error("Ошибка при обработке файла %s: %s", file, e)
