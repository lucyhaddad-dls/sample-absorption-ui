from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit)
import logging
from pint import Unit

log = logging.getLogger(__name__)

class SingleInputField(QWidget):
    def __init__(self, parent = None,
                 name:str|None = None,
                 value:str|float|int = None,
                 unit:Unit|None = None):
        super(SingleInputField, self).__init__(parent)

        main_layout = QHBoxLayout()
   
        self.name = name
        self._value = str(value)
        if isinstance(unit, Unit):
            self._unit = unit._repr_html_()
        else: self._unit = unit

        self.parent = parent

        main_layout.addWidget(QLabel(text = self.name))
        self.text_edit = QLineEdit(text = self.value)
        main_layout.addWidget(self.text_edit)
        if self.unit is not None:
            self.unit_edit = QLabel(text = self.unit)
            main_layout.addWidget(self.unit_edit)

        self.setLayout(main_layout)

        self.text_edit.editingFinished.connect(self.on_value_change)
        
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if isinstance(val, (float, int)):
            self._value = f"{val:.5g}"
        if isinstance(val, str):
            self._value = val
        return self._value

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, val):
        if val is None:
            self._unit = val
        if isinstance(val, str):
            self._unit = val
        if isinstance(val, Unit):
            self._unit = val._repr_html_()
       
        return self._unit

    def change_text_and_unit(self):
        """
        Update the text + unit fields.
        """
        self.text_edit.setText(self.value)
        if self.unit is not None:
            self.unit_edit.setText(self.unit)

    def on_value_change(self):
        self.value = self.text_edit.text()

        if self.name in ["formula", "edge", "absorber"]:
            remake_sample = True
        else:
            remake_sample = False
        self.parent.main_window.sample.on_value_change(self.name, self.value, remake_sample)
        self.parent.on_value_change()
    
    def update_text_and_unit(self):
        """
        Set `value` and `unit` to match the parent's \
        `sample` object and update text + unit fields.
        """
        value, unit = self.parent.main_window.sample.get_name_and_unit(self.name) 
        self.value = value
        self.unit = unit
        self.change_text_and_unit()