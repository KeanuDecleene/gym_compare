from PyQt6.QtWidgets import QMainWindow, QDialog, QListWidgetItem
from PyQt6.QtCore import Qt
from gui.main_window_setup import GymCompareSetup
from gui.custom_dialogs import emptyInputDialog
import requests

class GymCompare(QMainWindow):
    """Main window for the Gym Compare application."""
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.drag_pos = None
        self.setup = GymCompareSetup(self)

    def mousePressEvent(self, event):
        """Initiate window dragging if on header of window"""
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
        """Handle window dragging."""
        if self.drag_pos is not None and (event.buttons() & Qt.MouseButton.LeftButton):
            self.move(self.pos() + (event.globalPosition() - self.drag_pos).toPoint())
            self.drag_pos = event.globalPosition()

    def mouseReleaseEvent(self, event):
        """Clear drag state on release to avoid dragging unintentionally."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = None
        return super().mouseReleaseEvent(event)

    def search(self, input_address):
        """Handle search button click."""

        #empty input
        if input_address == "":
            dlg = emptyInputDialog(self)
            dlg.exec()
            return
        
        print(f"Searching for gyms near: {input_address}")

    def clear(self):
        """Clear the gym listbox, and restore placeholder text."""
        self.gym_list_box.clear()

        #placeholder restore
        item = QListWidgetItem(self.placeholder_text)
        item.setFlags(Qt.ItemFlag.NoItemFlags)
        self.gym_list_box.addItem(item)


        