from gui.base_window import BaseWindow
from gui.ui.ui_untitled import Ui_MainWindow
from config.config import Task


class MainWindow(BaseWindow):
    def _setup_ui(self) -> None:
        """Обозначение главных переменных."""
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Test')

    def _connect_widget(self) -> None:
        """Подключение виджетов к функциям."""
        self.ui.pushButton.clicked.connect(self._run)

    def _connect_bridge_signals(self) -> None:
        """Подключение сигналов из моста."""
        self.bridge.process_signal.connect(self._update_progress)
        self.bridge.done_signal.connect(self._done_scan)

    # --- реализация приложения ---
    def _run(self) -> None:
        self.bridge.send_task(Task('scanning'))

    def _update_progress(self, result) -> None:
        self.ui.progressBar.setValue(result.progress)

    def _done_scan(self, result):
        self.ui.progressBar.setValue(result.progress)
