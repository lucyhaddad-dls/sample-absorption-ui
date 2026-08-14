from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                               QComboBox, QCheckBox)
from PySide6.QtCore import Qt
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

from .elements_checkbox import ElementsCheckbox
import numpy as np
from sample_mass_calcs.measurements import Measurement
import logging
from typing import Literal

log = logging.getLogger(__name__)

class MplCanvas(FigureCanvasQTAgg):
    """
    Make a single matplotlib figure.
    """
    def __init__(self,
                parent=None, 
                width:int=500,
                height:int=300):

        fig = Figure(figsize=(width, height))
        self.ax = fig.add_subplot()
        super().__init__(fig)

class XyPlot(QWidget):
    """
    Basic plot object.
    """
    def __init__(self, parent=None):
        super().__init__()

        layout = QVBoxLayout()
        self.canvas = MplCanvas(self)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot_xy(self, x:np.ndarray, 
                y:np.ndarray, 
                xlabel:str, 
                ylabel:str, 
                linenames:list[str]):
    
        self.canvas.ax.cla()
        x, y = self.check_xy(x, y)

        if len(linenames) == 1:
            if y.ndim > 1:
                self.canvas.ax.plot(x, y[0], label=linenames[0])
            else:
                self.canvas.ax.plot(x, y, label=linenames[0])
        else:
            for i in range(len(linenames)):
                self.canvas.ax.plot(x, y[i,:], label=linenames[i])
        
                self.canvas.ax.legend()

        self.canvas.ax.set_xlabel(xlabel)
        self.canvas.ax.set_ylabel(ylabel)
        self.canvas.draw_idle()

    def check_xy(self, x:np.ndarray|Measurement,
                 y:np.ndarray|Measurement)->tuple[np.ndarray, np.ndarray]:
        if hasattr(x, "value"):
            x = np.array(x.value)
        if isinstance(x, list):
            x = np.array(x)
        if hasattr(y, "value"):
            y = np.array(y.value)
        if isinstance(y, list):
            yout = []
            for yi in y:
                if hasattr(yi, "value"):
                    yout.append(yi.value)
                else:
                    yout.append(yi)
            y = np.array(yout)
 
        return x, y


class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        layout = QVBoxLayout()
        self.parent = parent
        self.sample = parent.sample
        self.elements = self.sample.sample.elements

        self.plot_options = QComboBox()
        self.plot_options.addItems(["mass abs. coef.",
                                       "linear abs. coef.",
                                       "total abs."])
        self.plot_options.setCurrentText("mass abs. coef.")

        self._plotmodes = {"mass abs. coef.":"mass",
                            "linear abs. coef.":"linear",
                            "total abs.":"total"}
        
        layout.addWidget(self.plot_options)
        
        self.plot = XyPlot(self)
        layout.addWidget(self.plot)

        elements = list([e.name for e in self.elements])

        self.checkbox_widget = ElementsCheckbox(self, elements)
        layout.addWidget(self.checkbox_widget)
    
        self.setLayout(layout)

        self.set_plot_option()

        self.plot_options.currentTextChanged.connect(self.set_plot_option)


    def set_plot_option(self):
        """
        Update `yPlot` and redraw plot if necessary.
        """
        
        ymode = self._plotmodes[self.plot_options.currentText()]
        if hasattr(self, "checked"):
            self.set_xydata(ymode)

    def set_xydata(self, ymode:Literal["mass", "linear", "total"]):
        x = self.sample.sample.energy

        self.checked = self.checkbox_widget.get_checked_names()
        y0 = [e.mass_absorption for e in self.elements if e.name in self.checked]

        if "∑ Elements" in self.checked:
            y0.append(self.sample.sample.mass_absorption)

        if ymode == "mass":
            y = y0
        if ymode == "linear":
            if hasattr(self.sample.sample, "density"):
                y = [yi * self.sample.sample.density for yi in y0]
            else:
                log.warning("Provide density.")
                self.plot_options.setCurrentText("mass")
                self.set_xydata()
        if ymode == "total":
            if hasattr(self.sample.sample, "density") and hasattr(self.sample.sample, "thickness"):
                y = [yi * self.sample.sample.density * self.sample.sample.thickness for yi in y0]
            else:
                log.warning("Provide density and area/thickness.")
                self.plot_options.setCurrentText("mass")
                self.set_xydata()

        xlabel, ylabel = self.set_xylabels(x, y)

        self.plot.plot_xy(x, y, xlabel, ylabel, self.checked)
 
    def set_xylabels(self, x, y):
        xlabel = ""; ylabel = ""
        if hasattr(x, "unit"):
            xlabel = x.unit
        if hasattr(y, "unit"):
            ylabel = y.unit
        if isinstance(y, list):
            if hasattr(y[0], "unit"): ylabel = y[0].unit

        return xlabel, ylabel

    def change_checkbox_names(self):
        if self.elements == self.parent.sample.sample.elements:
            return
        self.elements = self.parent.sample.sample.elements
        names = [e.name for e in self.elements]
        self.checkbox_widget.change_checkbox_names(names)

    def handle_element_checkstate(self):
        self.checked = self.checkbox_widget.get_checked_names()
        self.set_plot_option()