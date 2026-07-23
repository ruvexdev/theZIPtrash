import sys
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QFileDialog, QCheckBox,
    QFrame, QMessageBox, QComboBox, QWidget, QGroupBox,
)

from src import autostart


class SettingsDialog(QDialog):
    def __init__(self, config, watcher, parent=None):
        super().__init__(parent)
        self.config = config
        self.watcher = watcher
        self.setWindowTitle("Settings - theZIPtrash")
        self.setMinimumSize(550, 480)
        self.setModal(True)
        self._build_ui()
        self._load_values()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Settings")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        folders_group = self._build_folders_section()
        layout.addWidget(folders_group)

        options_group = self._build_options_section()
        layout.addWidget(options_group)

        layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setObjectName("settingsBtn")
        btn_cancel.setFixedWidth(100)
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)

        btn_save = QPushButton("Save")
        btn_save.setFixedWidth(100)
        btn_save.clicked.connect(self._save)
        btn_layout.addWidget(btn_save)

        layout.addLayout(btn_layout)

    def _build_folders_section(self):
        group = QGroupBox("Monitored folders")
        group.setStyleSheet("""
            QGroupBox {
                font-size: 13px;
                font-weight: bold;
                color: #b388ff;
                border: 1px solid #2d2d5e;
                border-radius: 8px;
                padding: 16px 12px 12px 12px;
                margin-top: 8px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 6px;
            }
        """)
        layout = QVBoxLayout(group)

        self.folder_list = QListWidget()
        self.folder_list.setMaximumHeight(160)
        layout.addWidget(self.folder_list)

        btn_row = QHBoxLayout()
        btn_add = QPushButton("+ Add folder")
        btn_add.setObjectName("restoreBtn")
        btn_add.setCursor(Qt.PointingHandCursor)
        btn_add.clicked.connect(self._add_folder)
        btn_row.addWidget(btn_add)

        btn_remove = QPushButton("- Remove selected")
        btn_remove.setObjectName("deleteBtn")
        btn_remove.setCursor(Qt.PointingHandCursor)
        btn_remove.clicked.connect(self._remove_folder)
        btn_row.addWidget(btn_remove)

        btn_row.addStretch()
        layout.addLayout(btn_row)

        return group

    def _build_options_section(self):
        group = QGroupBox("Options")
        group.setStyleSheet("""
            QGroupBox {
                font-size: 13px;
                font-weight: bold;
                color: #b388ff;
                border: 1px solid #2d2d5e;
                border-radius: 8px;
                padding: 16px 12px 12px 12px;
                margin-top: 8px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 6px;
            }
        """)
        layout = QVBoxLayout(group)

        interval_row = QHBoxLayout()
        interval_label = QLabel("Scan every:")
        interval_row.addWidget(interval_label)

        self.interval_combo = QComboBox()
        self.interval_combo.addItems(["5 seconds", "10 seconds", "15 seconds", "30 seconds"])
        self.interval_combo.setFixedWidth(140)
        interval_row.addWidget(self.interval_combo)
        interval_row.addStretch()
        layout.addLayout(interval_row)

        if sys.platform == "win32":
            self.auto_start_cb = QCheckBox("Start automatically with Windows")
            layout.addWidget(self.auto_start_cb)
        else:
            self.auto_start_cb = None

        self.pause_cb = QCheckBox("Pause monitoring")
        layout.addWidget(self.pause_cb)

        return group

    def _load_values(self):
        for folder in self.config.watched_folders:
            self.folder_list.addItem(folder)

        interval = self.config.scan_interval
        interval_map = {5: 0, 10: 1, 15: 2, 30: 3}
        idx = interval_map.get(interval, 1)
        self.interval_combo.setCurrentIndex(idx)

        if self.auto_start_cb and autostart.is_available():
            self.auto_start_cb.setChecked(autostart.is_enabled())

        self.pause_cb.setChecked(self.config.monitoring_paused)

    def _add_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Select folder to monitor"
        )
        if folder:
            existing = [self.folder_list.item(i).text() for i in range(self.folder_list.count())]
            if folder not in existing:
                self.folder_list.addItem(folder)

    def _remove_folder(self):
        current = self.folder_list.currentRow()
        if current >= 0:
            self.folder_list.takeItem(current)

    def _save(self):
        folders = [self.folder_list.item(i).text() for i in range(self.folder_list.count())]
        self.config.watched_folders = folders

        interval_text = self.interval_combo.currentText()
        seconds = int(interval_text.split()[0])
        self.config.scan_interval = seconds

        if self.auto_start_cb and autostart.is_available():
            if self.auto_start_cb.isChecked():
                autostart.enable()
            else:
                autostart.disable()
            self.config.auto_start = self.auto_start_cb.isChecked()

        paused = self.pause_cb.isChecked()
        self.config.monitoring_paused = paused

        if paused:
            self.watcher.pause()
        else:
            self.watcher.resume()

        self.accept()
