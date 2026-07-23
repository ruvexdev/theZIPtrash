DARK_THEME = """
QMainWindow, QDialog {
    background-color: #1a1a2e;
    color: #e0e0e0;
}

QWidget {
    background-color: #1a1a2e;
    color: #e0e0e0;
    font-family: "Segoe UI", "Arial", sans-serif;
    font-size: 13px;
}

QLabel {
    color: #e0e0e0;
    background: transparent;
}

QLabel#titleLabel {
    color: #b388ff;
    font-size: 20px;
    font-weight: bold;
    background: transparent;
}

QLabel#subtitleLabel {
    color: #9e9e9e;
    font-size: 12px;
    background: transparent;
}

QLabel#statusLabel {
    font-size: 12px;
    padding: 4px 12px;
    border-radius: 10px;
    background-color: #2d1b69;
    color: #b388ff;
}

QLabel#statusLabelActive {
    background-color: #1b5e20;
    color: #81c784;
}

QLabel#statusLabelPaused {
    background-color: #e65100;
    color: #ffb74d;
}

QLabel#countLabel {
    color: #b388ff;
    font-size: 28px;
    font-weight: bold;
    background: transparent;
}

QLabel#countSubLabel {
    color: #9e9e9e;
    font-size: 11px;
    background: transparent;
}

QTableWidget {
    background-color: #16213e;
    alternate-background-color: #1a2744;
    border: 1px solid #2d2d5e;
    border-radius: 8px;
    gridline-color: #2d2d5e;
    selection-background-color: #3a1f7e;
    selection-color: #ffffff;
    outline: none;
}

QTableWidget::item {
    padding: 8px 12px;
    border-bottom: 1px solid #2d2d5e;
}

QTableWidget::item:selected {
    background-color: #3a1f7e;
}

QHeaderView::section {
    background-color: #16213e;
    color: #b388ff;
    border: none;
    border-bottom: 2px solid #7b2ff7;
    padding: 10px 12px;
    font-weight: bold;
    font-size: 12px;
}

QScrollBar:vertical {
    background-color: #1a1a2e;
    width: 10px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background-color: #7b2ff7;
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #9d4edd;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: #1a1a2e;
    height: 10px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal {
    background-color: #7b2ff7;
    border-radius: 5px;
    min-width: 30px;
}

QPushButton {
    background-color: #7b2ff7;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 8px 20px;
    font-weight: bold;
    font-size: 12px;
}

QPushButton:hover {
    background-color: #9d4edd;
}

QPushButton:pressed {
    background-color: #6a1fd4;
}

QPushButton:disabled {
    background-color: #3a3a5c;
    color: #666680;
}

QPushButton#restoreBtn {
    background-color: #2e7d32;
}

QPushButton#restoreBtn:hover {
    background-color: #43a047;
}

QPushButton#deleteBtn {
    background-color: #c62828;
}

QPushButton#deleteBtn:hover {
    background-color: #e53935;
}

QPushButton#settingsBtn {
    background-color: transparent;
    border: 1px solid #7b2ff7;
    color: #b388ff;
}

QPushButton#settingsBtn:hover {
    background-color: #2d1b69;
}

QPushButton#pauseBtn {
    background-color: #e65100;
}

QPushButton#pauseBtn:hover {
    background-color: #f57c00;
}

QPushButton#resumeBtn {
    background-color: #1b5e20;
}

QPushButton#resumeBtn:hover {
    background-color: #2e7d32;
}

QLineEdit {
    background-color: #16213e;
    color: #e0e0e0;
    border: 1px solid #2d2d5e;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 12px;
}

QLineEdit:focus {
    border: 1px solid #7b2ff7;
}

QListWidget {
    background-color: #16213e;
    border: 1px solid #2d2d5e;
    border-radius: 8px;
    outline: none;
}

QListWidget::item {
    padding: 8px 12px;
    border-bottom: 1px solid #2d2d5e;
}

QListWidget::item:selected {
    background-color: #3a1f7e;
    color: #ffffff;
}

QListWidget::item:hover {
    background-color: #1a2744;
}

QCheckBox {
    color: #e0e0e0;
    spacing: 8px;
    background: transparent;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 2px solid #7b2ff7;
    background-color: #16213e;
}

QCheckBox::indicator:checked {
    background-color: #7b2ff7;
    border-color: #7b2ff7;
}

QCheckBox::indicator:hover {
    border-color: #9d4edd;
}

QComboBox {
    background-color: #16213e;
    color: #e0e0e0;
    border: 1px solid #2d2d5e;
    border-radius: 6px;
    padding: 6px 12px;
    min-width: 80px;
}

QComboBox:hover {
    border-color: #7b2ff7;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox QAbstractItemView {
    background-color: #16213e;
    color: #e0e0e0;
    border: 1px solid #2d2d5e;
    selection-background-color: #3a1f7e;
}

QFrame#separator {
    background-color: #2d2d5e;
    max-height: 1px;
}

QFrame#headerFrame {
    background-color: #16213e;
    border-radius: 10px;
    padding: 16px;
}

QFrame#footerFrame {
    background-color: #16213e;
    border-radius: 10px;
    padding: 10px 16px;
}

QToolTip {
    background-color: #2d1b69;
    color: #e0e0e0;
    border: 1px solid #7b2ff7;
    border-radius: 4px;
    padding: 6px 10px;
    font-size: 11px;
}

QLabel#creditsLabel {
    color: #666680;
    font-size: 10px;
    background: transparent;
    padding: 4px 0px;
}
"""
