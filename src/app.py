import sys
import logging
from pathlib import Path

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from src.config import Config
from src.watcher import WatcherThread
from src.tray import SystemTray
from src.ui.main_window import MainWindow
from src.ui.styles import DARK_THEME
from src.zipper import limpiar_trash

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        self.app.setApplicationName("theZIPtrash")
        self.app.setApplicationDisplayName("theZIPtrash")
        self.app.setStyleSheet(DARK_THEME)

        self.config = Config()

        eliminated, remaining = limpiar_trash(self.config)
        if eliminated:
            logger.info(f"Cleaned {len(eliminated)} ZIPs from previous sessions")

        self.watcher = WatcherThread(self.config)
        self.watcher.zip_moved.connect(self._on_zip_moved)
        self.watcher.status_changed.connect(self._on_status_changed)

        self.main_window = MainWindow(self.config, self.watcher)
        self.tray = SystemTray(self.config, self.watcher)

        self.tray.show_window.connect(self._show_window)
        self.tray.quit_app.connect(self._quit)

        self.main_window.hide()

    def run(self):
        self.tray.show()
        self.watcher.start()

        if self.config.monitoring_paused:
            self.watcher.pause()
            self.main_window.update_status("paused")

        self.tray.show_message(
            "theZIPtrash",
            "Monitoreo de ZIPs activo. Doble clic en el icono para abrir.",
        )

        return self.app.exec_()

    def _on_zip_moved(self, entry):
        count = len(self.config.deleted_zips)
        self.main_window.refresh_table()
        self.tray.update_count(count)
        self.tray.show_message(
            "ZIP movido a la papelera",
            f"{entry.get('name', 'Unknown')} movido correctamente.",
        )

    def _on_status_changed(self, status):
        self.main_window.update_status(status)
        self.tray.update_pause_state()

    def _show_window(self):
        self.main_window.refresh_table()
        count = len(self.config.deleted_zips)
        self.tray.update_count(count)
        self.main_window.show()
        self.main_window.raise_()
        self.main_window.activateWindow()

    def _quit(self):
        self.watcher.stop()
        self.tray.hide()
        self.app.quit()
