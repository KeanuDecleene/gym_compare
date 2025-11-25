from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt
from gui.main_window_setup import GymCompareSetup
import requests

class GymCompare(QMainWindow):
    """Main window for the Gym Compare application."""
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.setup = GymCompareSetup(self)


    def mousePressEvent(self, event):
        """Enable window dragging hovering over header."""
        if event.button() == Qt.MouseButton.LeftButton:
            if self.header.underMouse():
                self.drag_pos = event.globalPosition()
            else:
                self.drag_pos = None

    def mouseMoveEvent(self, event):
        """Enable window dragging."""
        if self.drag_pos and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(self.pos() + (event.globalPosition() - self.drag_pos).toPoint())
            self.drag_pos = event.globalPosition()

    def find_gyms(self):
        """Function to handle gym search."""
        
    def get_gyms_near_location(self, location):
        """Function to fetch gyms near a location."""
        