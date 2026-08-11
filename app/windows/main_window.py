from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout,
                               QLabel, QTextEdit, QMainWindow)

from .formula_sample import FormulaWindow

class MainWindow(QMainWindow):
    """
    Main window for the mass app.
    """
    def __init__(self):
        super().__init__()
        self.setGeometry(500, 300, 1000, 600)

        self.setWindowTitle("MAIN WINDOW")

        self.widget = FormulaWindow(self)
        self.setCentralWidget(self.widget)

        self.show()