from PySide6.QtWidgets import QFileDialog

from gui.base_window import BaseWindow
from gui.ui.ui_untitled import Ui_MainWindow
from config.config import Task, Status


class MainWindow(BaseWindow):
    def _setup_ui(self) -> None:
        """Обозначение главных переменных."""
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Test')

        # При любом изменении пути мы всегда должны отправлять задачу с инициализацией (подключить сигнал изменения label)
        self.path_to_dir = r'C:/Users/notebook/Desktop/test_LocalAgent'
        self.ui.label.setText(self.path_to_dir)
        self.bridge.send_task(Task('init', self.path_to_dir))

    def _connect_widget(self) -> None:
        """Подключение виджетов к функциям."""
        self.ui.pushButton.clicked.connect(self._run_init)
        self.ui.pbt_scan.clicked.connect(self._run_scan)
        self.ui.pbt_vector.clicked.connect(self._run_vector)

    def _connect_bridge_signals(self) -> None:
        """Подключение сигналов из моста."""
        self.bridge.process_signal.connect(self._check_signal)
        self.bridge.done_signal.connect(self._check_signal)

    # --- реализация приложения ---
    def _run_init(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку с заметками")
        if folder == '':
            return
        self.path_to_dir = folder
        self.ui.label.setText(self.path_to_dir)
        self.bridge.send_task(Task('init', self.path_to_dir))
        self.ui.progressBar_scan.setValue(0)
        self.ui.progressBar_vector.setValue(0)

    def _run_vector(self):
        self.bridge.send_task(Task('vector', self.path_to_dir))

    def _run_scan(self):
        self.bridge.send_task(Task('scanning', self.path_to_dir))

    def _check_signal(self, result):
        if result.data['worker'] == 'scanning':
            if result.status == Status.RUN:
                self.ui.progressBar_scan.setValue(result.progress)
        elif result.data['worker'] == 'vector':
            self.ui.progressBar_vector.setValue(result.progress)
