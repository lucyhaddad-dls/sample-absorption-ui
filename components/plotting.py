from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                               QComboBox)
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from numpy import ndarray
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

    def plot_xy(self,
                x:Measurement|ndarray|list,
                y:Measurement|ndarray|list):
        """
        Clear `canvas.ax` and plot xy data.
        """
        if isinstance(x, Measurement):
            xlabel = x.unit._repr_latex_()
            xplot = x.value
        else:
            xlabel = ""; xplot = x
        if isinstance(y, Measurement):
            ylabel = y.unit._repr_latex_()
            yplot = y.value
        else:
            ylabel = ""; yplot = y

        self.canvas.ax.cla()
        self.canvas.ax.plot(xplot, yplot)
        self.canvas.ax.set_xlabel(f"{xlabel}")
        self.canvas.ax.set_ylabel(f"{ylabel}")

        self.canvas.draw_idle()

class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        layout = QVBoxLayout()
        self.parent = parent

        self.plot = XyPlot(self)
        layout.addWidget(self.plot)

        self.setLayout(layout)

        self.redraw_plot()

    def get_xy(self,
            x_key:str="energy",
            y_key:str="mass_absorption"):
        # change these later,,,!!!
        try:
            self.x = getattr(self.parent.main_window.sample.sample, x_key)
        except:
            self.x = np.empty((10))
            log.warning(f"No value for {x_key}")
        try:
            self.y = getattr(self.parent.main_window.sample.sample, y_key)
        except:
            self.y = np.empty_like(self.x)
            log.warning(f"No value for {y_key}")

    def redraw_plot(self):
        self.get_xy()
        self.plot.plot_xy(self.x, self.y)
        