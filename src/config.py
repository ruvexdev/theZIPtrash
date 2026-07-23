import json
import os
import shutil
from datetime import datetime
from pathlib import Path


class Config:
    APP_NAME = "theZIPtrash"
    APP_DIR = Path(os.environ.get("APPDATA", Path.home())) / APP_NAME
    CONFIG_FILE = APP_DIR / "config.json"
    TRASH_DIR = APP_DIR / "trash"

    @staticmethod
    def _default_watched_folders():
        home = Path.home()
        folders = []
        downloads = home / "Downloads"
        if downloads.exists():
            folders.append(str(downloads))
        desktop = home / "Desktop"
        if desktop.exists():
            folders.append(str(desktop))
        return folders

    DEFAULT_CONFIG = {
        "watched_folders": None,
        "scan_interval": 10,
        "auto_start": False,
        "monitoring_paused": False,
        "deleted_zips": [],
        "ignored_zips": [],
    }

    def __init__(self):
        self._ensure_dirs()
        self.config = self._load()

    def _ensure_dirs(self):
        self.APP_DIR.mkdir(parents=True, exist_ok=True)
        self.TRASH_DIR.mkdir(parents=True, exist_ok=True)

    def _load(self):
        if self.CONFIG_FILE.exists():
            try:
                with open(self.CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                merged = dict(self.DEFAULT_CONFIG)
                merged.update(data)
                if merged["watched_folders"] is None:
                    merged["watched_folders"] = self._default_watched_folders()
                if "ignored_zips" not in merged:
                    merged["ignored_zips"] = []
                return merged
            except (json.JSONDecodeError, OSError):
                return dict(self.DEFAULT_CONFIG)
        default = dict(self.DEFAULT_CONFIG)
        default["watched_folders"] = self._default_watched_folders()
        return default

    def save(self):
        with open(self.CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)

    @property
    def watched_folders(self):
        return self.config.get("watched_folders", [])

    @watched_folders.setter
    def watched_folders(self, folders):
        self.config["watched_folders"] = folders
        self.save()

    @property
    def scan_interval(self):
        return self.config.get("scan_interval", 10)

    @scan_interval.setter
    def scan_interval(self, seconds):
        self.config["scan_interval"] = max(2, int(seconds))
        self.save()

    @property
    def auto_start(self):
        return self.config.get("auto_start", False)

    @auto_start.setter
    def auto_start(self, value):
        self.config["auto_start"] = bool(value)
        self.save()

    @property
    def monitoring_paused(self):
        return self.config.get("monitoring_paused", False)

    @monitoring_paused.setter
    def monitoring_paused(self, value):
        self.config["monitoring_paused"] = bool(value)
        self.save()

    @property
    def deleted_zips(self):
        return self.config.get("deleted_zips", [])

    def add_watched_folder(self, path):
        path = str(Path(path).resolve())
        if path not in self.config["watched_folders"]:
            self.config["watched_folders"].append(path)
            self.save()
            return True
        return False

    def remove_watched_folder(self, path):
        path = str(Path(path))
        before = len(self.config["watched_folders"])
        self.config["watched_folders"] = [
            f for f in self.config["watched_folders"] if str(Path(f)) != path
        ]
        if len(self.config["watched_folders"]) < before:
            self.save()
            return True
        return False

    def record_deleted_zip(self, original_path, trash_path, name):
        entry = {
            "original_path": str(original_path),
            "trash_path": str(trash_path),
            "name": name,
            "date": datetime.now().isoformat(),
        }
        self.config["deleted_zips"].append(entry)
        self.save()
        return entry

    def remove_deleted_zip_record(self, trash_path):
        trash_path = str(trash_path)
        self.config["deleted_zips"] = [
            z for z in self.config["deleted_zips"] if z["trash_path"] != trash_path
        ]
        self.save()

    def get_deleted_zip_by_trash_path(self, trash_path):
        trash_path = str(trash_path)
        for z in self.config["deleted_zips"]:
            if z["trash_path"] == trash_path:
                return z
        return None

    @property
    def ignored_zips(self):
        return self.config.get("ignored_zips", [])

    def add_ignored_zip(self, zip_name, original_folder):
        entry = {"name": zip_name, "folder": str(original_folder)}
        if entry not in self.config["ignored_zips"]:
            self.config["ignored_zips"].append(entry)
            self.save()

    def is_zip_ignored(self, zip_name, folder_path):
        folder_path = str(folder_path)
        for ignored in self.config.get("ignored_zips", []):
            if ignored["name"] == zip_name and ignored["folder"] == folder_path:
                return True
        return False
