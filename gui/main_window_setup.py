from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QStyle
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon


class GymCompareSetup:
    """Handles creating all widgets and layouts for GymCompare."""

    def __init__(self, parent):
        self.parent = parent
        self.setup_window()
        self.setup_header()
        self.setup_layout()

    def setup_window(self):
        """Main window properties."""
        self.parent.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.parent.setMinimumSize(960, 540)

    def setup_header(self):
        """Create the custom title bar."""
        header = QWidget()
        header.setObjectName("header")
        header.setFixedHeight(40)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(8)

        #title
        title = QLabel("GYM COMPARE")
        title.setObjectName("headerTitle")
        layout.addWidget(title)
        layout.addStretch()

        #close button
        close_btn = QPushButton()
        close_btn.setObjectName("headerClose")
        close_btn.setFixedSize(28, 28)
        close_btn.setIcon(QIcon("gui/icons/close_button.png"))
        
        close_btn.setIconSize(QSize(15, 15))
        close_btn.clicked.connect(self.parent.close)

        layout.addWidget(close_btn)

        self.parent.header = header

    def setup_layout(self):
        """Attach header + main content to the QMainWindow."""
        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        #header
        root_layout.addWidget(self.parent.header)

        #main content
        content = QWidget()
        content.setObjectName("mainContent")
        root_layout.addWidget(content)

        self.parent.setCentralWidget(root)
