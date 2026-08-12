from PySide6.QtWidgets import (QWidget, QComboBox, QLabel, QHBoxLayout)
from sample_mass_calcs.measurements import units
from functools import partial


class UnitDropdownWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        unit_options = {
            "length":
                {"options":[units.nm, units.um, units.cm, units.m],
                 "title":"Thickness", "attr":"length_unit"},
            "mass":
                {"options":[units.ug, units.mg, units.g, units.kg],
                 "title":"Mass", "attr":"mass_unit"},
            "energy":
                {"options":[units.ev, units.gev, units.Mev],
                "title":"Energy", "attr":"energy_unit"}
            }

        layout = QHBoxLayout()
        layout.addWidget(QLabel("Units"))

        for key, val in unit_options.items():
            tmp = self.UnitDropdownBar(self, val)
            layout.addWidget(tmp)

        self.setLayout(layout)


    class UnitDropdownBar(QWidget):
        def __init__(self, parent, options:dict):
            super().__init__()
            self.widget = parent

            layout = QHBoxLayout()
            layout.addWidget(QLabel(options["title"]))
            self.dropdown = QComboBox()

            self._options = options

            choices = [i._repr_html_() for i in self._options["options"]]
            self.dropdown.addItems(choices)
            layout.addWidget(self.dropdown)
            self.get_parent_unit()
            self.setLayout(layout)

            self.dropdown.currentTextChanged.connect(self.update_parent_unit)

        def get_parent_unit(self):
            attr = self._options["attr"]
            val = getattr(self.widget.parent.main_window.sample.sample, attr)
            val = val._repr_html_()
            self.dropdown.setCurrentText(val)

        def update_parent_unit(self, v:str):
            self.widget.parent.main_window.sample.on_unit_change(self._options["attr"], v)
            self.widget.parent.on_unit_change()
