from PySide6.QtWidgets import (QWidget, QCheckBox, QVBoxLayout, QLabel)
from PySide6.QtCore import Qt

class ElementsCheckbox(QWidget):
    def __init__(self, parent, labels:list[str]):
        super().__init__()

        self.parent = parent
        self._sum_text = "∑ Elements"

        self._checkboxes = []
        self.layout = QVBoxLayout()
        
        for element in labels:
            self.make_checkbox(text = element)
        self.make_checkbox(text = self._sum_text)

        self.setLayout(self.layout)

    def make_checkbox(self, text:str):
        """
        Make single checkbox, connect to parent's `handle_element_checkstate()`
        method and add to `layout` + `_checkboxes`.
        """
        checkbox = QCheckBox(text = text)
        checkbox.checkStateChanged.connect(self.parent.handle_element_checkstate)
        self._checkboxes.append(checkbox)
        self.layout.addWidget(checkbox)
        

    def get_checked_names(self)->list[str]:
        """
        Get list of names of checked checkboxes.
        """
        checked = [c.text() for c in self._checkboxes if c.checkState() == Qt.CheckState.Checked]
        return checked

    def change_checkbox_names(self, labels):
        """
        Update the layout with old names being removed and
        new ones added.
        """
        to_remove = [c for c in self._checkboxes if c.text() not in labels]
        rm_text = [c.text() for c in to_remove]
        to_add = [l for l in labels if l not in [c.text() for c in self._checkboxes]]
        [self._checkboxes.remove(w) for w in to_remove]

        for i in range(self.layout.count()):
            item_tmp = self.layout.itemAt(i)
            if item_tmp == None: continue
            widget_tmp = item_tmp.widget()
            if widget_tmp.text() in rm_text:
                self.layout.itemAt(i).widget().deleteLater()

        for a in to_add:
            self.make_checkbox(text = a)
        self.make_checkbox(text = self._sum_text)
        self.layout.update()
