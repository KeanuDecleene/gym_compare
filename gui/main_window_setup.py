from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QListWidget
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon


class GymCompareSetup:
    """Handles creating all widgets and layouts for GymCompare."""
    def __init__(self, parent):
        self.parent = parent
        self.setup_window()
        self.setup_header()
        self.setup_address_bar()
        self.setup_list_box()
        self.setup_layout()


    def setup_window(self):
        """Main window properties."""
        self.parent.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.parent.setMinimumSize(960, 540)


    def setup_layout(self):
        """Attach header + main content to the QMainWindow."""
        root = QWidget()
        root.setObjectName("rootWidget")
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        #add widgets to root layout
        root_layout.addWidget(self.parent.header)
        root_layout.addWidget(self.parent.address_widget)
        root_layout.addWidget(self.parent.gym_list_container)

        self.parent.setCentralWidget(root)


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


    def setup_address_bar(self):
        """Address bar with search button"""
        address_container = QWidget()
        address_container.setObjectName("addressBarContainer")
        address_container.setFixedHeight(50)

        #set layout for container
        layout = QHBoxLayout(address_container)
        layout.setContentsMargins(10, 0, 10, 0)
        
        #address input
        address_text_box = QLineEdit()
        address_text_box.setObjectName("addressTextBox")
        address_text_box.setPlaceholderText("Enter Address...")
        address_text_box.setFixedHeight(32)    

        #search button
        search_btn = QPushButton("Search")
        search_btn.setObjectName("searchButton")
        search_btn.setFixedHeight(32) 
        search_btn.clicked.connect(lambda: self.parent.search(address_text_box.text()))      

        layout.addWidget(address_text_box)
        layout.addWidget(search_btn)

        self.parent.address_widget = address_container
        self.parent.address_bar = address_text_box
        self.parent.search_btn = search_btn
        
    def setup_list_box(self):
        """Create the list box for displaying gyms."""
        gym_list = QListWidget()
        gym_list.setObjectName("gymListBox")

        gym_list_container = QWidget()
        gym_list_container_layout = QVBoxLayout(gym_list_container)
        gym_list_container_layout.setContentsMargins(40, 20, 40, 50)
        gym_list_container_layout.addWidget(gym_list)

        self.parent.gym_list_box = gym_list
        self.parent.gym_list_container = gym_list_container


