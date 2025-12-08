"""Custom dialog implementations for the Gym Compare application."""

import sys
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox
from PyQt6.QtCore import Qt


class emptyInputDialog(QDialog):
    """Dialog to inform the user of empty input."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Empty Input")
        self.setFixedSize(300, 100)

        with open("gui/dialog_styles.qss", "r") as style:
            qss = style.read()
            self.setStyleSheet(qss)
        
        layout = QVBoxLayout()
        message = QLabel("Please enter an address.")
        layout.addWidget(message)
        
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)
        
        self.setLayout(layout)


    