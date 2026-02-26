import sys
import os
from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    # style.qss yolu (stabil)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    style_path = os.path.join(base_dir, "ui", "style.qss")
    if os.path.exists(style_path):
        with open(style_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())

    w = MainWindow()
    w.resize(1200, 700)
    w.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
