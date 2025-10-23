from gui.base_window import BaseWindow
from gui.ui.ui_untitled import Ui_MainWindow
from config.config import Task


class MainWindow(BaseWindow):
    def _setup_ui(self) -> None:
        """Обозначение главных переменных."""
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Test')

        # При любом изменении пути мы всегда должны отправлять задачу с инициализацией (подключить сигнал изменения label)
        self.path_to_dir = r'C:/Users/notebook/Desktop/test_LocalAgent'
        self.bridge.send_task(Task('init', self.path_to_dir))

    def _connect_widget(self) -> None:
        """Подключение виджетов к функциям."""
        self.ui.pushButton.clicked.connect(self._run)

    def _connect_bridge_signals(self) -> None:
        """Подключение сигналов из моста."""
        self.bridge.process_signal.connect(self._update_progress)
        self.bridge.done_signal.connect(self._done_scan)

    # --- реализация приложения ---
    def _run(self) -> None:
        self.ui.pushButton.setEnabled(True)
        self.bridge.send_task(Task('scanning', self.path_to_dir))

    def _update_progress(self, result) -> None:
        self.ui.progressBar.setValue(result.progress)

    def _done_scan(self, result):
        self.ui.pushButton.setFlat(False)
        self.ui.progressBar.setValue(result.progress)
