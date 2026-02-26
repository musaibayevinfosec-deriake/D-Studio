from __future__ import annotations

from PySide6.QtCore import QEasingCurve, QPropertyAnimation, Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget,
    QFrame, QToolButton, QStyle, QGraphicsDropShadowEffect
)

from core.app_state import AppState
from ui.cleaner_page import CleanerPage
from ui.dashboard_page import DashboardPage


def add_shadow(widget: QWidget, blur: int = 22, alpha: int = 80, y: int = 10):
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(blur)
    shadow.setOffset(0, y)
    shadow.setColor(Qt.black)
    # Qt.black default alpha 255; bunu azaltmaq üçün color yaratmaq istəsən:
    # shadow.setColor(QColor(0, 0, 0, alpha))
    widget.setGraphicsEffect(shadow)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("D-Studio")

        # (Opsional) daha glass hissi üçün:
        # self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.state = AppState()

        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(14)

        # ===== Sidebar (glass card) =====
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(240)

        add_shadow(self.sidebar, blur=28, alpha=80, y=10)

        sb = QVBoxLayout(self.sidebar)
        sb.setContentsMargins(12, 12, 12, 12)
        sb.setSpacing(10)

        # Collapse button (top)
        self.btn_collapse = QToolButton()
        self.btn_collapse.setObjectName("CollapseButton")
        self.btn_collapse.setIcon(self.style().standardIcon(QStyle.SP_TitleBarShadeButton))
        self.btn_collapse.setIconSize(QSize(18, 18))
        self.btn_collapse.setCheckable(True)
        self.btn_collapse.setToolTip("Collapse sidebar")
        sb.addWidget(self.btn_collapse, alignment=Qt.AlignLeft)

        # Nav buttons
        self.btn_clean = self._nav_button(
            text="  Clean",
            icon=self.style().standardIcon(QStyle.SP_DialogResetButton),
        )
        self.btn_dash = self._nav_button(
            text="  Dashboard",
            icon=self.style().standardIcon(QStyle.SP_ComputerIcon),
        )

        self.btn_clean.setChecked(True)

        sb.addWidget(self.btn_clean)
        sb.addWidget(self.btn_dash)
        sb.addStretch(1)

        # ===== Pages =====
        self.stack = QStackedWidget()
        self.clean_page = CleanerPage(self.state)
        self.dash_page = DashboardPage(self.state)
        self.stack.addWidget(self.clean_page)  # 0
        self.stack.addWidget(self.dash_page)   # 1

        # Wrap stack in a "card" container for consistent styling
        self.content_card = QFrame()
        self.content_card.setObjectName("Card")
        add_shadow(self.content_card, blur=30, alpha=90, y=12)

        content_layout = QVBoxLayout(self.content_card)
        content_layout.setContentsMargins(14, 14, 14, 14)
        content_layout.addWidget(self.stack)

        layout.addWidget(self.sidebar, 0)
        layout.addWidget(self.content_card, 1)

        # ===== Signals =====
        self.btn_clean.clicked.connect(self.go_clean)
        self.btn_dash.clicked.connect(self.go_dashboard)

        self.clean_page.data_changed.connect(self.dash_page.refresh_from_state)

        self.btn_collapse.toggled.connect(self.toggle_sidebar)

        # Animation
        self._sb_anim = QPropertyAnimation(self.sidebar, b"minimumWidth")
        self._sb_anim.setDuration(220)
        self._sb_anim.setEasingCurve(QEasingCurve.OutCubic)

        self._sb_anim2 = QPropertyAnimation(self.sidebar, b"maximumWidth")
        self._sb_anim2.setDuration(220)
        self._sb_anim2.setEasingCurve(QEasingCurve.OutCubic)

    def _nav_button(self, text: str, icon: QIcon) -> QToolButton:
        btn = QToolButton()
        btn.setObjectName("NavButton")
        btn.setText(text)
        btn.setIcon(icon)
        btn.setIconSize(QSize(18, 18))
        btn.setCheckable(True)
        btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        btn.setAutoExclusive(True)
        return btn

    def go_clean(self):
        self.btn_clean.setChecked(True)
        self.stack.setCurrentIndex(0)

    def go_dashboard(self):
        self.btn_dash.setChecked(True)
        self.dash_page.refresh_from_state()
        self.stack.setCurrentIndex(1)

    def toggle_sidebar(self, collapsed: bool):
        expanded_w = 240
        collapsed_w = 64

        start = self.sidebar.width()
        end = collapsed_w if collapsed else expanded_w

        # switch style (icons-only when collapsed)
        if collapsed:
            self.btn_clean.setToolButtonStyle(Qt.ToolButtonIconOnly)
            self.btn_dash.setToolButtonStyle(Qt.ToolButtonIconOnly)
            self.btn_collapse.setIcon(self.style().standardIcon(QStyle.SP_TitleBarUnshadeButton))
        else:
            self.btn_clean.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.btn_dash.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.btn_collapse.setIcon(self.style().standardIcon(QStyle.SP_TitleBarShadeButton))

        self._sb_anim.stop()
        self._sb_anim2.stop()

        self._sb_anim.setStartValue(start)
        self._sb_anim.setEndValue(end)

        self._sb_anim2.setStartValue(start)
        self._sb_anim2.setEndValue(end)

        self._sb_anim.start()
        self._sb_anim2.start()
