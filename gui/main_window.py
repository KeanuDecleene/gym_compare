from PyQt6.QtWidgets import QMainWindow, QDialog, QListWidgetItem, QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import QThread, Qt, QSize
from gui.main_window_setup import GymCompareSetup
from gui.components.custom_dialogs import EmptyInputDialog, OverpassTimeoutDialog, NoGymsFoundDialog


from logic.address import Address
from logic.pipeline import GymPipeline
import requests

from logic.search_worker import SearchWorker


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
        if input_address.strip() == "":
            dlg = EmptyInputDialog(self)
            dlg.exec()
            return

        self.search_btn.setEnabled(False)
        self.search_btn.setText("Searching...")

        self.thread = QThread()
        self.worker = SearchWorker(input_address)

        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.handle_search_results)
        self.worker.error.connect(self.handle_search_error)

        self.worker.finished.connect(self.thread.quit)
        self.worker.error.connect(self.thread.quit)

        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.error.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def handle_search_results(self, gyms):
        self.search_btn.setEnabled(True)
        self.search_btn.setText("Search")

        if len(gyms) == 0:
            dlg = NoGymsFoundDialog(self)
            dlg.exec()
            return

        self.gym_list_box.clear()
        self.add_gym_list_header()

        for gym in gyms:
            item = QListWidgetItem()
            item.setSizeHint(QSize(0, 32))
            item.setData(Qt.ItemDataRole.UserRole, gym)

            widget = self.create_gym_list_item(gym)

            self.gym_list_box.addItem(item)
            self.gym_list_box.setItemWidget(item, widget)




    def handle_search_error(self, error_type):
        self.search_btn.setEnabled(True)
        self.search_btn.setText("Search")

        if error_type == "timeout":
            dlg = OverpassTimeoutDialog(self)
            result = dlg.exec()
            if result == QDialog.DialogCode.Accepted:
                self.search(self.address_bar.text())
            return

        if error_type == "http":
            dlg = OverpassTimeoutDialog(self)
            dlg.exec()
            return

        print(f"Unexpected error: {error_type}")

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

        price = QLabel(gym.price_per_week or "N/A")
        price.setObjectName("gymPrice")

        latitiude = gym.latitude
        longitude = gym.longitude
        
        name.setFixedWidth(180)
        address.setFixedWidth(360)
        distance.setFixedWidth(90)
        price.setFixedWidth(90)

        distance.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        layout.addWidget(name)
        layout.addWidget(address)
        layout.addWidget(distance)
        layout.addWidget(price)

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
        price = QLabel("Price:")

        name.setFixedWidth(180)
        address.setFixedWidth(360)
        distance.setFixedWidth(90)
        price.setFixedWidth(90)

        distance.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        for label in (name, address, distance, price):
            label.setStyleSheet("color: white;")

        layout.addWidget(name)
        layout.addWidget(address)
        layout.addWidget(distance)
        layout.addWidget(price)

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
        item = self.gym_list_box.currentItem()
        if not item or not item.data(Qt.ItemDataRole.UserRole):
            return
        item.latitude = item.data(Qt.ItemDataRole.UserRole).latitude
        item.longitude = item.data(Qt.ItemDataRole.UserRole).longitude



        print("viewing map" + str(item.latitude) + " " + str(item.longitude))



        #TODO select gym function and be able to press the view map button to open gym in browser on maps


    def export(self):
        """export the gym in current order to a pdf """
        print("exporting")
        
        #TODO export functionality to pdf



        