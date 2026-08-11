from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                               QComboBox)
from PySide6.QtCore import Qt
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
import numpy as np
from sample_mass_calcs.measurements import Measurement

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

class Plot2D(QWidget):
    def __init__(self, parent=None):
        super(Plot2D, self).__init__(parent)

        layout = QVBoxLayout()
        self.canvas = MplCanvas(self)
        layout.addWidget(self.canvas)
 
        self.setLayout(layout)

    def plot_xy(self,
                x:Measurement|np.ndarray|list,
                y:Measurement|np.ndarray|list):
        """
        Clear `canvas.ax` and plot `x` and `y` data.
        """
        
        if isinstance(x, Measurement):
            xlabel = x.unit._repr_latex_()
            xplot = x.value
        else:
            xlabel = ""
            xplot = x
        if isinstance(y, Measurement):
            ylabel = y.unit._repr_latex_()
            yplot = y.value
        else:
            ylabel = ""
            yplot = y

        self.canvas.ax.cla()
        self.canvas.ax.plot(xplot, yplot)
        self.canvas.ax.set_xlabel(f"{xlabel}")
        self.canvas.ax.set_ylabel(f"{ylabel}")
        self.canvas.draw_idle()


class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super(PlotWidget, self).__init__(parent)

        self.current_plot = "mass_absorption"

        tab_names = ["mass_absorption", 
                     "linear_absorption"]

        self.plot_options = QComboBox()
        self.plot_options.addItems(tab_names)
        
        layout = QVBoxLayout()
        self.parent = parent

        self.plot = Plot2D(self)
        layout.addWidget(self.plot)
        layout.addWidget(self.plot_options)

        self.setLayout(layout)

        x = parent.sample.energy
        y = getattr(parent.sample, self.current_plot)
        self.plot.plot_xy(x, y)

        self.plot_options.currentTextChanged.connect(self.on_plot_options_change)
        
    def on_plot_options_change(self, v):
        self.current_plot = v
        self.redraw_plot()

    def redraw_plot(self):
        self.plot.canvas.ax.cla() 
        x = self.parent.sample.energy
        try:
            y = getattr(self.parent.sample, self.current_plot)
            self.plot.plot_xy(x, y)
        except:
            y = np.empty_like(x.value)
            print("no value for: ", self.current_plot)
                   
        self.plot.canvas.draw_idle()
        