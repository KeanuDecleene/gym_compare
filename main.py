import sys 
from PyQt6.QtWidgets import QApplication
from gui.main_window import GymCompare

def main():
    """Main function to run the Gym Finder application."""
    app = QApplication(sys.argv)
    window = GymCompare()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
