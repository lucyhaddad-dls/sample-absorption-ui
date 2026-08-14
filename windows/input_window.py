from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout)
from components.input_fields import SingleInputField
from components.units_fields import UnitDropdownWidget
from components.plotting import PlotWidget

class InputWindow(QWidget):
    def __init__(self, parent=None):
        super(InputWindow, self).__init__(parent)

        main_layout = QHBoxLayout()

        self.main_window = parent
        self.sample = self.main_window.sample

        input_keys = [l for l in self.sample.sample_dict.keys()\
                       if "unit" not in l]

        vertical_layout = QVBoxLayout()
        self.units_widget = UnitDropdownWidget(self)
        vertical_layout.addWidget(self.units_widget)
   
        inputs_layout = QVBoxLayout()
        self._input_widgets = []
        for name in input_keys:
            val, unit = self.sample.get_name_and_unit(name)
            tmp = SingleInputField(parent = self,
                                   name = name, 
                                   value = val,
                                   unit = unit)
            inputs_layout.addWidget(tmp)
            self._input_widgets.append(tmp)
        vertical_layout.addLayout(inputs_layout)

        main_layout.addLayout(vertical_layout)

        self.plot_widget = PlotWidget(self)
        main_layout.addWidget(self.plot_widget)

        self.setLayout(main_layout)

    def on_value_change(self):
        for widget in self._input_widgets:
            widget.update_text_and_unit()
        self.plot_widget.change_checkbox_names()
        self.plot_widget.on_unit_change()