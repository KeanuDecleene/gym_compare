from PyQt6.QtWidgets import QMainWindow, QDialog, QListWidgetItem, QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, QSize
from gui.main_window_setup import GymCompareSetup
from gui.components.custom_dialogs import EmptyInputDialog, OverpassTimeoutDialog


from logic.address import Address
from logic.pipeline import GymPipeline
import requests


class GymCompare(QMainWindow):
    """main window for the Gym Compare application."""
    def __init__(self):
        """initialize the main window."""
        super().__init__()
        self.drag_pos = None
        self.setup = GymCompareSetup(self)

    def mousePressEvent(self, event):
        """initiate window dragging if on header of window"""
        if event.button() == Qt.MouseButton.LeftButton:
            widget = self.childAt(event.pos())
            # check if the click is within the header area and not the close button
            if widget is self.header or widget.parent() is self.header:
                if widget.objectName() == "headerClose":
                    self.drag_pos = None
                else:
                    self.drag_pos = event.globalPosition()
            else:
                self.drag_pos = None
                    
    def mouseMoveEvent(self, event):
        """handle window dragging."""
        if self.drag_pos is not None and (event.buttons() & Qt.MouseButton.LeftButton):
            self.move(self.pos() + (event.globalPosition() - self.drag_pos).toPoint())
            self.drag_pos = event.globalPosition()

    def mouseReleaseEvent(self, event):
        """clear drag state on release to avoid dragging unintentionally."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = None
        return super().mouseReleaseEvent(event)

    def search(self, input_address):
        """handle search button click."""
        #empty input dialog handler
        if input_address == "":
            dlg = EmptyInputDialog(self)
            dlg.exec()
            return
        
        #run the gym pipeline
        pipeline = GymPipeline()
        try:
            gyms = pipeline.run(input_address)
        
        except requests.exceptions.Timeout:
            dlg = OverpassTimeoutDialog(self)
            result = dlg.exec()
            if result == QDialog.DialogCode.Accepted:
                self.search(input_address)  #retry search
            return

        except requests.esceptions.HTTPError:
            dlg = OverpassTimeoutDialog(self)
            dlg.exec()
            return

        #set up list box for results
        self.gym_list_box.clear()
        self.add_gym_list_header()

        #populate listbox with gyms data
        for gym in gyms:
            item = QListWidgetItem()
            item.setSizeHint(QSize(0, 32))
            item.setData(Qt.ItemDataRole.UserRole, gym)

            widget = self.create_gym_list_item(gym)

            self.gym_list_box.addItem(item)
            self.gym_list_box.setItemWidget(item, widget)

    def create_gym_list_item(self, gym):
        """create a custom widget for a gym list item."""
        widget = QWidget()
        widget.setObjectName("gymRow")
        widget.setStyleSheet("background: transparent;")

        layout = QHBoxLayout(widget)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(16)

        name = QLabel(gym.name)
        name.setObjectName("gymName")

        address = QLabel(gym.address)
        address.setObjectName("gymAddress")

        distance = QLabel(f"{gym.distance_km:.2f} km")
        distance.setObjectName("gymDistance")

        name.setFixedWidth(180)
        address.setFixedWidth(360)
        distance.setFixedWidth(90)

        distance.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        layout.addWidget(name)
        layout.addWidget(address)
        layout.addWidget(distance)

        return widget
    
    def add_gym_list_header(self):
        """add header row to gym listbox."""
        header_widget = QWidget()
        header_widget.setObjectName("gymHeader")

        layout = QHBoxLayout(header_widget)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(16)

        name = QLabel("Gym:")
        address = QLabel("Address:")
        distance = QLabel("Distance:")

        name.setFixedWidth(180)
        address.setFixedWidth(360)
        distance.setFixedWidth(90)

        distance.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        for label in (name, address, distance):
            label.setStyleSheet("color: white;")

        layout.addWidget(name)
        layout.addWidget(address)
        layout.addWidget(distance)

        item = QListWidgetItem()
        item.setFlags(Qt.ItemFlag.NoItemFlags)
        item.setSizeHint(header_widget.sizeHint())

        self.gym_list_box.addItem(item)
        self.gym_list_box.setItemWidget(item, header_widget)

    def clear(self):
        """clear the gym listbox, and restore placeholder text."""
        self.gym_list_box.clear()

        #placeholder restore
        item = QListWidgetItem(self.placeholder_text)
        item.setFlags(Qt.ItemFlag.NoItemFlags)
        self.gym_list_box.addItem(item)


    def view_map(self):
        """view the map of selected gym from listbox"""
        print("viewing map")

        #TODO select gym function and be able to press the view map button to open gym in browser on maps


    def export(self):
        """export the gym in current order to a pdf """
        print("exporting")
        
        #TODO export functionality to pdf



        