from PyQt6.QtCore import QObject, QThread, pyqtSignal
import requests

from logic.pipeline import GymPipeline

class SearchWorker(QObject):
    """Worker class to perform gym search in a separate thread."""
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, address):
        super().__init__()
        self.address = address

    def run(self):
        pipeline = GymPipeline()
        try:
            gyms = pipeline.run(self.address)
            self.finished.emit(gyms)
        except requests.exceptions.Timeout:
            self.error.emit("timeout")
        except requests.exceptions.HTTPError:
            self.error.emit("http")
        except Exception as e:
            self.error.emit(str(e))