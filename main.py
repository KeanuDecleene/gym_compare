import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import GymCompare
from gui.utils import resource_path

def main():
    """main entry point for the application."""
    app = QApplication(sys.argv)

    qss_path = resource_path("gui/styles.qss")
    with open(qss_path, "r") as style_file:
        app.setStyleSheet(style_file.read())

    gym_compare = GymCompare()
    gym_compare.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
