import os
import sys
import time
import logging
import win32serviceutil
import win32service
import win32event
import servicemanager

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import Config
from src.zipper import detect_garbage_zips, move_to_trash, _get_file_size_str, _get_zip_size
from src.notifications import notify

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    filename=os.path.join(os.environ.get("APPDATA", "."), "theZIPtrash", "service.log"),
)
logger = logging.getLogger("theZIPtrash-service")


class ZIPTrashService(win32serviceutil.ServiceFramework):
    _svc_name_ = "theZIPtrash"
    _svc_display_name_ = "theZIPtrash - ZIP Monitor Service"
    _svc_description_ = "Monitors folders and moves extracted ZIP files to trash."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.config = None
        self.running = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.running = False
        win32event.SetEvent(self.stop_event)

    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, ""),
        )
        self.config = Config()
        self._clean_old_zips()
        self._run()

    def _clean_old_zips(self):
        from src.zipper import clean_trash
        eliminated, remaining = clean_trash(self.config)
        if eliminated:
            logger.info(f"Cleaned {len(eliminated)} old ZIPs from trash")

    def _run(self):
        while self.running:
            if self.config.monitoring_paused:
                time.sleep(1)
                continue

            try:
                self._scan()
            except Exception as e:
                logger.error(f"Scan error: {e}")

            interval = self.config.scan_interval
            for _ in range(interval):
                if not self.running:
                    break
                time.sleep(1)

    def _scan(self):
        trash_dir = self.config.TRASH_DIR
        for folder_str in self.config.watched_folders:
            folder = os.path.normpath(folder_str)
            if not os.path.isdir(folder):
                continue

            garbage_zips = detect_garbage_zips(folder)
            for zip_path in garbage_zips:
                if self.config.is_zip_ignored(zip_path.name, folder):
                    continue

                trash_path, error = move_to_trash(zip_path, trash_dir)
                if error:
                    logger.warning(f"Could not move {zip_path.name}: {error}")
                    continue

                size = _get_zip_size(trash_path)
                size_str = _get_file_size_str(size)

                self.config.record_deleted_zip(
                    original_path=zip_path,
                    trash_path=trash_path,
                    name=zip_path.name,
                )

                notify("ZIP moved (service)", f"{zip_path.name} ({size_str})")
                logger.info(f"Moved ZIP: {zip_path.name} ({size_str})")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(ZIPTrashService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(ZIPTrashService)
