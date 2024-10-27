from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer, QSize, QRect
from PyQt6.QtGui import QPainter, QColor, QPen

class LoadingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("")
        self.setFixedSize(200, 200)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        layout = QVBoxLayout(self)
        
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)
        self.timer.start(30)  # Update every 30ms for smooth animation
        
        self.label = QLabel("Sending email...", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
            QLabel {
                color: #9832C1;
                font-size: 14px;
                font-weight: bold;
                background: transparent;
                margin-top: 120px;
            }
        """)
        layout.addWidget(self.label)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Create semi-transparent background
        painter.setBrush(QColor(245, 245, 245, 230))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)
        
        # Draw spinning circle
        center = self.rect().center()
        size = 50
        rect = QRect(
            center.x() - size//2,
            center.y() - size//2,
            size,
            size
        )
        
        pen = QPen(QColor("#9832C1"), 4)
        painter.setPen(pen)
        
        # Draw arc - start angle is determined by self.angle
        # Length of arc is 270 degrees (leaving a small gap)
        start_angle = self.angle * 16  # Convert to 1/16th of a degree
        span_angle = 270 * 16
        painter.drawArc(rect, start_angle, span_angle)

    def rotate(self):
        self.angle = (self.angle - 10) % 360  # Rotate counterclockwise
        self.update()

    def closeEvent(self, event):
        self.timer.stop()
        super().closeEvent(event)

    def center_on_parent(self):
        if self.parent():
            parent_geo = self.parent().geometry()
            self.move(
                parent_geo.center().x() - self.width()//2,
                parent_geo.center().y() - self.height()//2
            )
