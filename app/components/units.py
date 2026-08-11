"""
Utils for unit conversions here
"""
from PySide6.QtWidgets import (QWidget, QComboBox, QLabel, QVBoxLayout,
                               QHBoxLayout)
from functools import partial

from sample_mass_calcs.measurements import units

length_units = [units.nm, units.um, units.cm, units.m]
mass_units = [units.ug, units.mg, units.g, units.kg]
energy_units = [units.ev, units.gev, units.Mev]


class UnitConversionWidget(QWidget):
    def __init__(self, parent=None):
        super(UnitConversionWidget, self).__init__(parent)
        self.parent = parent

        layout = QHBoxLayout()
        layout.addWidget(QLabel("Units"))

        length_layout = QHBoxLayout()
        length_layout.addWidget(QLabel("Length/Thickness"))
        self.length_unit_box = QComboBox()
        [self.length_unit_box.addItem(l._repr_html_()) for l in length_units]
        length_layout.addWidget(self.length_unit_box)

        mass_layout = QHBoxLayout()
        mass_layout.addWidget(QLabel("Mass"))
        self.mass_unit_box = QComboBox()
        [self.mass_unit_box.addItem(m._repr_html_()) for m in mass_units]
        mass_layout.addWidget(self.mass_unit_box)

        energy_layout = QHBoxLayout()
        energy_layout.addWidget(QLabel("Energy"))
        self.energy_unit_box = QComboBox()
        [self.energy_unit_box.addItem(e._repr_html_()) for e in energy_units]
        energy_layout.addWidget(self.energy_unit_box)
    
        layout.addLayout(length_layout)        
        layout.addLayout(mass_layout)
        layout.addLayout(energy_layout)

        self.length_unit_box.setCurrentText(self.parent.sample.length_unit._repr_html_())
        self.energy_unit_box.setCurrentText(self.parent.sample.energy_unit._repr_html_())
        self.mass_unit_box.setCurrentText(self.parent.sample.mass_unit._repr_html_())

        self.setLayout(layout)

        self.length_unit_box.currentTextChanged.connect(partial(self.on_change, mode="length"))
        self.energy_unit_box.currentTextChanged.connect(partial(self.on_change, mode = "energy"))
        self.mass_unit_box.currentTextChanged.connect(partial(self.on_change, mode = "mass"))

    def on_change(self, v, mode):
        if mode == "energy":
            self.parent.sample.energy_unit = getattr(units, v)
        elif mode == "length":
            self.parent.sample.length_unit = getattr(units, v)
        elif mode == "mass":
            self.parent.sample.mass_unit = getattr(units, v)

        self.parent.on_unit_change()