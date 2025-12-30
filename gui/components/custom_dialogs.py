"""Custom dialog implementations for the Gym Compare application."""

import sys
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox
from PyQt6.QtCore import Qt


class EmptyInputDialog(QDialog):
    """Dialog to inform the user of empty input."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Empty Input")
        self.setFixedSize(300, 100)

        with open("gui/components/dialog_styles.qss", "r") as style:
            qss = style.read()
            self.setStyleSheet(qss)
        
        layout = QVBoxLayout()
        message = QLabel("Please enter an address.")
        layout.addWidget(message)
        
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)
        
        self.setLayout(layout)

class NoGymsFoundDialog(QDialog):
    """Dialog shown when no gyms are found near the given address."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("No Gyms Found")
        self.setFixedSize(300, 100)

        with open("gui/components/dialog_styles.qss", "r") as style:
            qss = style.read()
            self.setStyleSheet(qss)
        
        layout = QVBoxLayout()
        message = QLabel("No gyms were found near the provided address.")
        layout.addWidget(message)
        
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)
        
        self.setLayout(layout)

class OverpassTimeoutDialog(QDialog):
    """Dialog shown when Overpass API times out."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Service Timeout")
        self.setFixedSize(360, 130)

        with open("gui/components/dialog_styles.qss", "r") as style:
            self.setStyleSheet(style.read())

        layout = QVBoxLayout()

        message = QLabel(
            "The map service is taking too long to respond.\n\n"
            "This is usually temporary.\nWould you like to try again?"
        )
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message.setWordWrap(True)

        layout.addWidget(message)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Retry |
            QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject) 

        layout.addWidget(buttons)
        self.setLayout(layout)


    