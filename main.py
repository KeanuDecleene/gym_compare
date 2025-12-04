import sys 
from PyQt6.QtWidgets import QApplication
from gui.main_window import GymCompare

def main():
    """Main function to run the Gym Finder application."""
    app = QApplication(sys.argv)

    #open styling to add to window
    with open("gui/styles.qss", "r") as style_file:
        qss = style_file.read()
        app.setStyleSheet(qss)

    gym_compare = GymCompare()
    gym_compare.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
