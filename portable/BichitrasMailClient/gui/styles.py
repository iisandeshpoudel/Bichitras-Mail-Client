STYLE_SHEET = """
QMainWindow {
    background-color: #F5F5F5;
}

QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #333333;
}

QLabel {
    color: #9832C1;
    font-weight: bold;
    font-size: 14px;
}

QLineEdit {
    padding: 10px;
    border: 2px solid #E0E0E0;
    border-radius: 8px;
    background-color: white;
    color: #333333;
    font-size: 13px;
    selection-background-color: #9832C1;
}

QLineEdit:focus {
    border: 2px solid #9832C1;
    background-color: white;
}

QTextEdit {
    padding: 10px;
    border: 2px solid #E0E0E0;
    border-radius: 8px;
    background-color: white;
    color: #333333;
    font-size: 13px;
    selection-background-color: #9832C1;
}

QTextEdit:focus {
    border: 2px solid #9832C1;
    background-color: white;
}

QPushButton {
    background-color: #9832C1;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
    font-weight: bold;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #8129BB;
}

QPushButton:pressed {
    background-color: #8639BC;
    padding-top: 11px;
    padding-bottom: 9px;
}

QPushButton#secondary {
    background-color: #E0E0E0;
    color: #333333;
}

QPushButton#secondary:hover {
    background-color: #D0D0D0;
}

QMessageBox {
    background-color: #F5F5F5;
    color: #333333;
}

QToolBar {
    border: none;
    background: white;
    padding: 8px;
    spacing: 8px;
    border-bottom: 1px solid #E0E0E0;
}

QToolBar QToolButton {
    background-color: transparent;
    border: none;
    border-radius: 4px;
    padding: 6px;
    color: #333333;
}

QToolBar QToolButton:hover {
    background-color: #F0F0F0;
}

QStatusBar {
    background: white;
    color: #9832C1;
    border-top: 1px solid #E0E0E0;
}

QTabWidget::pane {
    border: 2px solid #E0E0E0;
    border-radius: 8px;
    background-color: white;
}

QTabBar::tab {
    background: #F0F0F0;
    color: #333333;
    padding: 10px 20px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabBar::tab:selected {
    background: #9832C1;
    color: white;
}

QTabBar::tab:hover:!selected {
    background: #E0E0E0;
}

QComboBox {
    padding: 8px;
    border: 2px solid #E0E0E0;
    border-radius: 8px;
    background-color: white;
    color: #333333;
}

QComboBox:hover {
    border: 2px solid #9832C1;
}

QComboBox::drop-down {
    border: none;
}

QComboBox::down-arrow {
    image: url(down_arrow.png);
    width: 12px;
    height: 12px;
}

QListWidget {
    background-color: white;
    border: 2px solid #E0E0E0;
    border-radius: 8px;
}

QListWidget::item {
    padding: 8px;
    border-bottom: 1px solid #E0E0E0;
}

QListWidget::item:selected {
    background-color: #9832C1;
    color: white;
}
"""
