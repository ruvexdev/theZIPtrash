import sys
from pathlib import Path

from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PyQt5.QtWidgets import (
    QSystemTrayIcon, QMenu, QAction, QApplication,
)


def _create_tray_icon_pixmap(size=64):
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)

    painter.setBrush(QColor("#7b2ff7"))
    painter.setPen(Qt.NoPen)
    painter.drawRoundedRect(4, 4, size - 8, size - 8, 12, 12)

    painter.setPen(QColor("#ffffff"))
    font = QFont("Segoe UI", size // 3, QFont.Bold)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignCenter, "Z")

    painter.end()
    return pixmap


class SystemTray(QObject):
    show_window = pyqtSignal()
    quit_app = pyqtSignal()

    def __init__(self, config, watcher, parent=None):
        super().__init__(parent)
        self.config = config
        self.watcher = watcher

        icon_path = Path(__file__).resolve().parent.parent / "assets" / "icon.ico"
        if icon_path.exists():
            icon = QIcon(str(icon_path))
        else:
            icon = QIcon(QPixmap(_create_tray_icon_pixmap()))

        self.tray = QSystemTrayIcon(icon, QApplication.instance())
        self.tray.setToolTip("theZIPtrash - ZIP Monitor")

        self._build_menu()
        self.tray.activated.connect(self._on_activate)

    def _build_menu(self):
        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background-color: #16213e;
                color: #e0e0e0;
                border: 1px solid #2d2d5e;
                border-radius: 6px;
                padding: 4px;
            }
            QMenu::item {
                padding: 8px 24px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #3a1f7e;
            }
            QMenu::separator {
                height: 1px;
                background-color: #2d2d5e;
                margin: 4px 8px;
            }
        """)

        self.show_action = QAction("Open theZIPtrash")
        self.show_action.triggered.connect(self.show_window.emit)
        menu.addAction(self.show_action)

        menu.addSeparator()

        self.count_action = QAction("ZIPs in trash: 0")
        self.count_action.setEnabled(False)
        menu.addAction(self.count_action)

        menu.addSeparator()

        self.pause_action = QAction("Pause monitoring")
        self.pause_action.triggered.connect(self._toggle_pause)
        menu.addAction(self.pause_action)

        menu.addSeparator()

        quit_action = QAction("Quit")
        quit_action.triggered.connect(self.quit_app.emit)
        menu.addAction(quit_action)

        self.tray.setContextMenu(menu)

    def _on_activate(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_window.emit()

    def _toggle_pause(self):
        if self.config.monitoring_paused:
            self.config.monitoring_paused = False
            self.watcher.resume()
            self.pause_action.setText("Pause monitoring")
        else:
            self.config.monitoring_paused = True
            self.watcher.pause()
            self.pause_action.setText("Resume monitoring")

    def update_count(self, count):
        self.count_action.setText(f"ZIPs in trash: {count}")

    def update_pause_state(self):
        if self.config.monitoring_paused:
            self.pause_action.setText("Resume monitoring")
        else:
            self.pause_action.setText("Pause monitoring")

    def show_message(self, title, message):
        self.tray.showMessage(title, message, QSystemTrayIcon.Information, 3000)

    def show(self):
        self.tray.show()

    def hide(self):
        self.tray.hide()
