from PySide6.QtWidgets import (QWidget, QTextEdit, QDoubleSpinBox, QComboBox, QHBoxLayout,
                               QVBoxLayout, QLabel, QLineEdit)
from sample_mass_calcs.measurements import Measurement
import logging
from numpy import ndarray
from pint import Unit

log = logging.getLogger(__name__)


class InputBox(QWidget):
    def __init__(self, parent=None,
                 name:str|None=None,
                 initial:str|float|int=None,
                 unit:Unit|None=None):
        super(InputBox, self).__init__(parent)

        self.main_layout = QHBoxLayout()
        self.name = name
        self._value = str(initial)
        self.unit = unit
        self.sample = parent.parent.sample

        self.set_layout()
        self.setLayout(self.main_layout)

        self.text_edit.editingFinished.connect(self.on_change)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if isinstance(val, (float, int)):
            self._value = str(val)
        else:
            self._value = val
        return self._value

    def set_layout(self):
        self.main_layout.addWidget(QLabel(text=self.name))
        self.text_edit = QLineEdit(text=self.value)
        self.main_layout.addWidget(self.text_edit)
        if self.unit is not None:
            self.unit_edit = QLabel(text=self.unit._repr_html_())
            self.main_layout.addWidget(self.unit_edit)

    def change_vals(self):
        self.text_edit.setText(self.value)
        if self.unit is not None:
            self.unit_edit.setText(self.unit._repr_html_())

    def on_change(self):
        # could do some checks here to be fair..
        self.value = self.text_edit.text()
      
        dtype = type(getattr(self.sample, self.name))
        if isinstance(dtype, (str, float, int)):
            setattr(self.sample, self.name, dtype(self.value))
        else:
            new = Measurement(float(self.value), _unit = self.unit)
            setattr(self.sample, self.name, new)
           

class InputBoxes(QWidget):
    def __init__(self, parent=None,
                 names:list[str]|None=None):
        super().__init__()

        self.parent = parent
        self._names = names

        layout = QVBoxLayout()
        self._widgets = {}
        for name in self._names:
            val, unit = self.get_sample_value(name)
            if isinstance(val, bool):
                continue
            self._widgets[name] = InputBox(parent=self,
                                           name = name,
                                           initial = val,
                                           unit = unit)
            layout.addWidget(self._widgets[name])
        self.setLayout(layout)
            

    def get_sample_value(self, name:str)->tuple[None|str|bool|float, None|Unit]:
        try:
            out = getattr(self.parent.sample, name)
        except:
            log.warning(f"{name} is not in Sample Object")
            value = None; unit = None
        if isinstance(out, ndarray):
            value = False; unit = None
        if isinstance(out, Measurement):
            value = out.value; unit = out.unit
        else:
            value = out; unit = None
        return value, unit

    def on_sample_change(self):
        for name in self._widgets.keys():
            value, unit = self.get_sample_value(name)
            self._widgets[name].value = value
            self._widgets[name].unit = unit
            self._widgets[name].change_vals()