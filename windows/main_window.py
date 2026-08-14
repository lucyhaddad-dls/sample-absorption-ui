from PySide6.QtWidgets import QMainWindow
from .input_window import InputWindow
from utils.sample import SampleBuilder

class MainWindow(QMainWindow):
    """
    Main window for app, all sample information \
    lives here.
    """
    def __init__(self):
        super().__init__()
        self.setGeometry(500, 300, 1000, 600)

        self.setWindowTitle("MAIN WINDOW")

        self.sample = SampleBuilder()
        self.input_window = InputWindow(self)
        self.setCentralWidget(self.input_window)

        self.show()