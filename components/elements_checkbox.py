# stack of checkboxes that can be added / deleted at choice:

from PySide6.QtWidgets import (QWidget, QCheckBox, QVBoxLayout)
from PySide6.QtCore import Qt

class ElementsCheckbox(QWidget):
    def __init__(self, parent, labels:list[str]):
        super().__init__()

        self.parent = parent

        self._sum_txt = "∑ Elements"
        labels.append(self._sum_txt)

        self.layout = QVBoxLayout()
        self._checkboxes = []

        for element in labels:
            tmp = QCheckBox(text = element)
            self._checkboxes.append(tmp)
            tmp.checkStateChanged.connect(parent.handle_element_checkstate)
            self.layout.addWidget(tmp)

        self._checkboxes[-1].setCheckState(Qt.CheckState.Checked)
        self.setLayout(self.layout)

    def get_checked_names(self)->list[str]:
        checked = [c.text() for c in self._checkboxes if c.checkState() == Qt.CheckState.Checked]
        return checked

    def change_checkbox_names(self, new_labels:list[str]):

        labels = new_labels + [self._sum_txt]

        [tmp.setCheckState(Qt.CheckState.Unchecked) for tmp in self._checkboxes if tmp.text() != self._sum_txt]

        to_remove = [r for r in [c.text() for c in self._checkboxes] if r not in labels]
        for i in range(len(self._checkboxes)):
            if self._checkboxes[i].text() in to_remove:
                self._checkboxes.pop(i)
                p = self.layout.takeAt(i)
                del p

        to_add = [l for l in labels if l not in [c.text() for c in self._checkboxes]]
        for name in to_add:
            tmp = QCheckBox(text = name)
            self._checkboxes.append(tmp)
            tmp.checkStateChanged.connect(self.parent.handle_element_checkstate)
            self.layout.addWidget(tmp)