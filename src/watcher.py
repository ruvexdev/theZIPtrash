import logging
import time
from pathlib import Path

from PyQt5.QtCore import QThread, pyqtSignal

from src.config import Config
from src.notifications import notificar
from src.zipper import detectar_zips_basura, mover_a_trash, _get_file_size_str, _get_zip_size

logger = logging.getLogger(__name__)


class WatcherThread(QThread):
    zip_moved = pyqtSignal(dict)
    scan_complete = pyqtSignal(int)
    error_occurred = pyqtSignal(str)
    status_changed = pyqtSignal(str)

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self._running = True
        self._paused = False

    def run(self):
        self.status_changed.emit("active")
        while self._running:
            if self._paused:
                time.sleep(1)
                continue

            try:
                self._scan()
            except Exception as e:
                logger.error(f"Scan error: {e}")
                self.error_occurred.emit(str(e))

            interval = self.config.scan_interval
            for _ in range(interval * 10):
                if not self._running:
                    break
                time.sleep(0.1)

        self.status_changed.emit("stopped")

    def _scan(self):
        folders = self.config.watched_folders
        trash_dir = self.config.TRASH_DIR
        found_count = 0

        for folder_str in folders:
            folder = Path(folder_str)
            if not folder.exists() or not folder.is_dir():
                continue

            garbage_zips = detectar_zips_basura(folder)

            for zip_path in garbage_zips:
                if self.config.is_zip_ignored(zip_path.name, folder):
                    continue

                trash_path, error = mover_a_trash(zip_path, trash_dir)

                if error:
                    logger.warning(f"Could not move {zip_path.name}: {error}")
                    continue

                size = _get_zip_size(trash_path)
                size_str = _get_file_size_str(size)

                entry = self.config.record_deleted_zip(
                    original_path=zip_path,
                    trash_path=trash_path,
                    name=zip_path.name,
                )
                entry["size_str"] = size_str

                notificar(
                    "ZIP movido a la papelera",
                    f"{zip_path.name} ({size_str})\nOriginal: {folder}",
                )

                self.zip_moved.emit(entry)
                found_count += 1

        self.scan_complete.emit(found_count)

    def pause(self):
        self._paused = True
        self.status_changed.emit("paused")

    def resume(self):
        self._paused = False
        self.status_changed.emit("active")

    def stop(self):
        self._running = False
        self.wait(3000)
