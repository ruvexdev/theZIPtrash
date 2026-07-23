import os
from datetime import datetime
from pathlib import Path

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QFrame, QMessageBox, QAbstractItemView,
)

from src.config import Config
from src.zipper import restaurar_zip, eliminar_permanente


class MainWindow(QMainWindow):
    def __init__(self, config, watcher, parent=None):
        super().__init__(parent)
        self.config = config
        self.watcher = watcher
        self.setWindowTitle("theZIPtrash")
        self.setMinimumSize(850, 550)
        self.resize(850, 550)

        icon_path = Path(__file__).resolve().parent.parent.parent / "assets" / "icon.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        self._build_ui()
        self.refresh_table()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        header = self._build_header()
        layout.addWidget(header)

        self.table = self._build_table()
        layout.addWidget(self.table, 1)

        footer = self._build_footer()
        layout.addWidget(footer)

        credits = QLabel("Made by: ruvexdev-official with opencode \u2764")
        credits.setObjectName("creditsLabel")
        credits.setAlignment(Qt.AlignCenter)
        layout.addWidget(credits)

    def _build_header(self):
        frame = QFrame()
        frame.setObjectName("headerFrame")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(20, 16, 20, 16)

        left = QVBoxLayout()
        title = QLabel("theZIPtrash")
        title.setObjectName("titleLabel")
        left.addWidget(title)

        subtitle = QLabel("ZIPs basura detectados y gestionados automaticamente")
        subtitle.setObjectName("subtitleLabel")
        left.addWidget(subtitle)
        layout.addLayout(left)

        right = QVBoxLayout()
        right.setAlignment(Qt.AlignRight | Qt.AlignCenter)

        self.count_label = QLabel("0")
        self.count_label.setObjectName("countLabel")
        self.count_label.setAlignment(Qt.AlignCenter)
        right.addWidget(self.count_label)

        count_sub = QLabel("en papelera")
        count_sub.setObjectName("countSubLabel")
        count_sub.setAlignment(Qt.AlignCenter)
        right.addWidget(count_sub)
        layout.addLayout(right)

        return frame

    def _build_table(self):
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Nombre", "Tamano", "Fecha", "Original", ""])
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.verticalHeader().setVisible(False)
        table.setShowGrid(False)

        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setMinimumSectionSize(80)

        table.setRowHeight(0, 42)

        return table

    def _build_footer(self):
        frame = QFrame()
        frame.setObjectName("footerFrame")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(16, 10, 16, 10)

        self.status_label = QLabel("Monitoreo: Activo")
        self.status_label.setObjectName("statusLabel")
        layout.addWidget(self.status_label)

        layout.addStretch()

        btn_settings = QPushButton("Configuracion")
        btn_settings.setObjectName("settingsBtn")
        btn_settings.setFixedWidth(120)
        btn_settings.clicked.connect(self._open_settings)
        layout.addWidget(btn_settings)

        btn_delete_all = QPushButton("Eliminar todo")
        btn_delete_all.setObjectName("deleteBtn")
        btn_delete_all.setFixedWidth(120)
        btn_delete_all.clicked.connect(self._delete_all)
        layout.addWidget(btn_delete_all)

        return frame

    def refresh_table(self):
        deleted = self.config.deleted_zips
        self.table.setRowCount(len(deleted))
        self.count_label.setText(str(len(deleted)))

        for row, entry in enumerate(deleted):
            name = entry.get("name", "Unknown")
            trash_path = Path(entry.get("trash_path", ""))

            if trash_path.exists():
                size = os.path.getsize(trash_path)
                size_str = self._format_size(size)
            else:
                size_str = "N/A"

            date_str = entry.get("date", "")
            if date_str:
                try:
                    dt = datetime.fromisoformat(date_str)
                    date_str = dt.strftime("%d/%m/%Y %H:%M")
                except ValueError:
                    pass

            original = entry.get("original_path", "N/A")

            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(size_str))
            self.table.setItem(row, 2, QTableWidgetItem(date_str))
            self.table.setItem(row, 3, QTableWidgetItem(original))

            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setContentsMargins(4, 2, 4, 2)
            btn_layout.setSpacing(4)

            btn_restore = QPushButton("Restaurar")
            btn_restore.setObjectName("restoreBtn")
            btn_restore.setFixedHeight(28)
            btn_restore.setCursor(Qt.PointingHandCursor)
            btn_restore.clicked.connect(lambda _, e=entry: self._restore(e))
            btn_layout.addWidget(btn_restore)

            btn_delete = QPushButton("X")
            btn_delete.setObjectName("deleteBtn")
            btn_delete.setFixedSize(28, 28)
            btn_delete.setCursor(Qt.PointingHandCursor)
            btn_delete.clicked.connect(lambda _, e=entry: self._delete_single(e))
            btn_layout.addWidget(btn_delete)

            self.table.setCellWidget(row, 4, btn_widget)
            self.table.setRowHeight(row, 42)

    def update_status(self, status):
        if status == "active":
            self.status_label.setText("Monitoreo: Activo")
            self.status_label.setObjectName("statusLabel")
            self.status_label.setStyleSheet(
                "background-color: #1b5e20; color: #81c784; padding: 4px 12px; border-radius: 10px; font-size: 12px;"
            )
        elif status == "paused":
            self.status_label.setText("Monitoreo: Pausado")
            self.status_label.setStyleSheet(
                "background-color: #e65100; color: #ffb74d; padding: 4px 12px; border-radius: 10px; font-size: 12px;"
            )
        elif status == "stopped":
            self.status_label.setText("Monitoreo: Detenido")
            self.status_label.setStyleSheet(
                "background-color: #c62828; color: #ef9a9a; padding: 4px 12px; border-radius: 10px; font-size: 12px;"
            )

    def _restore(self, entry):
        success, error = restaurar_zip(entry, self.config)
        if success:
            self.refresh_table()
            self._show_info("Restaurado", f"'{entry['name']}' restaurado correctamente.")
        else:
            self._show_error("Error", f"No se pudo restaurar: {error}")

    def _delete_single(self, entry):
        reply = QMessageBox.question(
            self, "Eliminar permanentemente",
            f"Eliminar '{entry['name']}' permanentemente?\nEsta accion no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            success, error = eliminar_permanente(entry["trash_path"])
            if success:
                self.config.remove_deleted_zip_record(entry["trash_path"])
                self.refresh_table()
            else:
                self._show_error("Error", f"No se pudo eliminar: {error}")

    def _delete_all(self):
        deleted = self.config.deleted_zips
        if not deleted:
            self._show_info("Vacio", "No hay ZIPs en la papelera.")
            return

        reply = QMessageBox.question(
            self, "Eliminar todo",
            f"Eliminar {len(deleted)} ZIP(s) permanentemente?\nEsta accion no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            errors = []
            for entry in list(deleted):
                success, error = eliminar_permanente(entry["trash_path"])
                if success:
                    self.config.remove_deleted_zip_record(entry["trash_path"])
                else:
                    errors.append(f"{entry['name']}: {error}")
            self.refresh_table()
            if errors:
                self._show_error("Errores", "\n".join(errors))

    def _open_settings(self):
        from src.ui.settings_dialog import SettingsDialog
        dialog = SettingsDialog(self.config, self.watcher, self)
        if dialog.exec_():
            self.refresh_table()

    def _show_info(self, title, message):
        QMessageBox.information(self, title, message)

    def _show_error(self, title, message):
        QMessageBox.critical(self, title, message)

    @staticmethod
    def _format_size(size_bytes):
        for unit in ("B", "KB", "MB", "GB"):
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"

    def closeEvent(self, event):
        event.ignore()
        self.hide()
