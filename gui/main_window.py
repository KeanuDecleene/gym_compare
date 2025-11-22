from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
import requests

class GymCompare(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gym Compare")
        self.setMinimumSize(960, 540)

        layout = QVBoxLayout()

        self.setLayout(layout)

    def find_gyms(self):
        """Function to handle gym search."""
        

    def get_gyms_near_location(self, location):
        """Function to fetch gyms near a location."""
        