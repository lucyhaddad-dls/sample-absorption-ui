from PySide6.QtWidgets import (QWidget, QLabel, QTextEdit,
                               QHBoxLayout, QVBoxLayout, QComboBox)

from sample_mass_calcs.xas_sample import XRaySample
from components.input_box import InputBoxes
from components.plotting import PlotWidget
from numpy import ndarray
from components.units import UnitConversionWidget

class FormulaWindow(QWidget):
    def __init__(self, parent=None):
        super(FormulaWindow, self).__init__(parent)

        self.main_layout = QHBoxLayout()
        self.sample = XRaySample(formula="TiO", absorber="Ti", edge="K")

        units_widget = UnitConversionWidget(self)
 
        self.input = ["formula", "absorber", "edge", "mu_total",
        "density", "area", "thickness", "mass"]

        vlayout = QVBoxLayout()
        vlayout.addWidget(units_widget)

        self.input_boxes = InputBoxes(self, self.input)

        vlayout.addWidget(self.input_boxes)

        self.plot = PlotWidget(parent=self)

        self.main_layout.addLayout(vlayout)

        self.main_layout.addWidget(self.plot)

        self.setLayout(self.main_layout)

    def on_unit_change(self):
        self.plot.redraw_plot()
        self.input_boxes.on_sample_change()
