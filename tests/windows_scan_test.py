from pathlib import Path
from unittest import TestCase, main
from unittest.mock import Mock, patch, MagicMock

from core.scanning.windows_scan import WindowsScanner


class WindowsScannerTest(TestCase):
    def setUp(self):
        self.db_mock = Mock()
        self.scanner = WindowsScanner("C:/vault", self.db_mock)
        self.scanner.logger = Mock()

    @patch("core.scanning.windows_scan.Path.exists", return_value=False)
    def test_scan_no_vault(self, exists_mock):
        result = list(self.scanner.scan())

        self.assertEqual(result, [0])
        self.scanner.logger.debug.assert_called_with(
            "Не существует директории по указанному пути: %s", "C:/vault"
        )

    @patch("core.scanning.windows_scan.Path.exists", return_value=True)
    @patch("core.scanning.windows_scan.Path.rglob", return_value=[])
    def test_scan_empty_folder(self, rglob_mock, exists_mock):
        result = list(self.scanner.scan())

        self.assertEqual(result, [100])
        self.scanner.logger.debug.assert_called_with("В папке не найдены файлы")

    @patch("core.scanning.windows_scan.hash_file", return_value="hash123")
    @patch("core.scanning.windows_scan.Path.exists", return_value=True)
    @patch("core.scanning.windows_scan.Path.rglob")
    def test_scan_with_files(self, rglob_mock, exists_mock, hash_mock):
        file1, file2, file3 = MagicMock(), MagicMock(), MagicMock()
        for i, f in enumerate([file1, file2, file3], start=1):
            f.is_file.return_value = True
            f.parts = ("C:", "vault", f"file{i}.txt")
            f.stat.return_value = Mock(st_mtime=i * 100)
            f.relative_to.return_value = Path(f"file{i}.txt")
        rglob_mock.return_value = [file1, file2, file3]

        # _db.get_file_by_path возвращает None (новый файл)
        self.db_mock.get_file_by_path.return_value = None

        result = list(self.scanner.scan())

        # test progress
        self.assertTrue(result[-1] == 100)
        self.assertGreaterEqual(len(result), 3)

        self.assertEqual(self.db_mock.add.call_count, 3)

    @patch("core.scanning.windows_scan.hash_file", return_value="abc123")
    def test_process_file_update(self, hash_mock):
        file_mock = MagicMock()
        file_mock.relative_to.return_value = Path("file.txt")
        file_mock.stat.return_value = Mock(st_mtime=1.23)

        # существующая запись, но с другим hash
        self.db_mock.get_file_by_path.return_value = {"hash": "old_hash"}

        self.scanner._process_file(Path("vault"), file_mock)

        self.db_mock.update.assert_called_once()
        self.db_mock.add.assert_not_called()

    @patch("core.scanning.windows_scan.hash_file", return_value="xyz")
    def test_process_file_add(self, hash_mock):
        file_mock = MagicMock()
        file_mock.relative_to.return_value = Path("file.txt")
        file_mock.stat.return_value = Mock(st_mtime=9.99)

        self.db_mock.get_file_by_path.return_value = None

        self.scanner._process_file(Path("vault"), file_mock)

        self.db_mock.add.assert_called_once()
        self.db_mock.update.assert_not_called()

    @patch("core.scanning.windows_scan.hash_file", side_effect=Exception("ошибка"))
    def test_process_file_exception(self, hash_mock):
        file_mock = MagicMock()
        file_mock.relative_to.return_value = Path('file.txt')

        self.scanner._process_file(Path('vault'), file_mock)

        self.scanner.logger.error.assert_called_once()
        self.scanner._db.add.assert_not_called()
        self.scanner._db.update.assert_not_called()


if __name__ == "__main__":
    main()
