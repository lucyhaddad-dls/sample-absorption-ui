from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                               QComboBox, QCheckBox)
from PySide6.QtCore import Qt
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from numpy import ndarray
from components.elements_checkbox import ElementsCheckbox
from sample_mass_calcs.measurements import Measurement
import numpy as np
import logging

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
        if len(linenames) == 1:
            self.canvas.ax.plot(x, y[0], label=linenames[0])
        else:
            for i in range(len(linenames)):
                self.canvas.ax.plot(x, y[i,:], label=linenames[i])
            self.canvas.ax.legend()

        self.canvas.ax.set_xlabel(xlabel)
        self.canvas.ax.set_ylabel(ylabel)
        self.canvas.draw_idle()


class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        layout = QVBoxLayout()
        self.parent = parent
        self.sample = parent.sample
        self.elements = self.sample.sample.elements

        self.plot = XyPlot(self)
        layout.addWidget(self.plot)

        elements = list([e.name for e in self.elements])

        self.checkbox_widget = ElementsCheckbox(self, elements)
        layout.addWidget(self.checkbox_widget)
        
    
        self.setLayout(layout)

    def change_checkbox_names(self):
        if self.elements == self.parent.sample.sample.elements:
            print("no change")
            return
        self.elements = self.parent.sample.sample.elements
        names = [e.name for e in self.elements]
        self.checkbox_widget.change_checkbox_names(names)


    def handle_element_checkstate(self):
        if hasattr(self, "checkbox_widget"):
            self.checked = self.checkbox_widget.get_checked_names()
        
            self.y = [e.mass_absorption for e in self.elements if e.name in self.checked]
            if "∑ Elements" in self.checked:
                self.y.append(self.sample.sample.mass_absorption)

            self.plot_multiple_elements()

    def check_x_y_types(self)->tuple[np.ndarray, np.ndarray, str, str]:
        xlabel = ""; ylabel = ""
        self.x = self.sample.sample.energy
        if hasattr(self.x, "value"):
            xplot = np.array(self.x.value); xlabel = self.x.unit
        else:
            xplot = np.array(self.x)

        if isinstance(self.y, list):
            yplot = []
            for val in self.y:
                if hasattr(val, "value"):
                    yplot.append(val.value); ylabel = val.unit
                else:
                    yplot.append(val)

            yplot = np.array(yplot)

        elif hasattr(self.y, "value"):
            yplot = np.array(self.y.value); ylabel = self.y.unit
        else:
            yplot = np.array(self.y)

        return xplot, yplot, xlabel, ylabel
                
    def plot_multiple_elements(self):
        if len(self.checked) >= 1:
            xplot, yplot, xlabel, ylabel = self.check_x_y_types()
            self.plot.plot_xy(xplot, yplot, xlabel, ylabel, self.checked)
        else:
            self.plot.canvas.ax.cla()
            self.plot.canvas.draw_idle()