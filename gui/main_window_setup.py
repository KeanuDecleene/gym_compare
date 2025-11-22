from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

class GymCompareSetup:
    """Handles creating all widgets and layouts for GymCompare."""
    def __init__(self, parent: QWidget):
        self.parent = parent
        self.setup_window()
        self.setup_header()
        self.setup_layout()

    def setup_window(self):
        """Set up the main window properties."""
        self.parent.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.parent.setMinimumSize(960, 540)

    def setup_header(self):
        """Set up the header."""
        self.parent.header = QWidget()
        self.parent.header.setObjectName("header")
        self.parent.header.setFixedHeight(30)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(10, 0, 10, 0)
        header_layout.setSpacing(5)
        self.parent.header.setLayout(header_layout)

        #title label
        self.parent.title_label = QLabel("Gym Compare")
        self.parent.title_label.setObjectName("headerTitle")
        header_layout.addWidget(self.parent.title_label)
        header_layout.addStretch()

        #close button
        self.parent.close_btn = QPushButton("X")
        self.parent.close_btn.setObjectName("headerClose")
        self.parent.close_btn.setFixedSize(25, 25)
        self.parent.close_btn.clicked.connect(self.parent.close)
        header_layout.addWidget(self.parent.close_btn)

    def setup_layout(self):
        """Set up the main layout of the window."""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.parent.header)

        #example content placeholder
        main_layout.addWidget(QLabel(""))

        self.parent.setLayout(main_layout)
