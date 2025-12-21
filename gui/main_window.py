from PyQt6.QtWidgets import QMainWindow, QDialog, QListWidgetItem
from PyQt6.QtCore import Qt
from gui.main_window_setup import GymCompareSetup
from gui.components.custom_dialogs import emptyInputDialog


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
            dlg = emptyInputDialog(self)
            dlg.exec()
            return
        
        #run the gym pipeline
        pipeline = GymPipeline()
        gyms = pipeline.run(input_address)

        if not gyms:
            #TODO add a dialog box to inform no gyms found
            item = QListWidgetItem("No gyms found.")
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.gym_list_box.addItem(item)
            return

        self.gym_list_box.clear()
        #populate listbox with gyms data
        for gym in gyms:
            #TODO FORMATTING THE LIST BOX BETTER AND ADDING A HEADER
            text =  (f"{gym.name} {gym.address} {gym.distance_km:.2f} km away")
            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, gym)
            self.gym_list_box.addItem(item)




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



        