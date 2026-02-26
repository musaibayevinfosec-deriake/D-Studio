from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

def add_shadow(widget, blur=22, alpha=90, y=10):
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(blur)
    shadow.setOffset(0, y)
    shadow.setColor(QColor(0, 0, 0, alpha))
    widget.setGraphicsEffect(shadow)

class KPICard(QFrame):
    def __init__(self, title, value):
        super().__init__()
        self.setObjectName("Card")
        add_shadow(self, blur=26, alpha=85, y=10)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(6)

        self.title = QLabel(title)
        self.value = QLabel(str(value))

        self.title.setObjectName("kpiTitle")
        self.value.setObjectName("kpiValue")

        layout.addWidget(self.title)
        layout.addWidget(self.value)

    def update_value(self, val):
        self.value.setText(str(val))
