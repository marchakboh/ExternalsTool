from PySide6.QtWidgets import (
    QVBoxLayout,
    QDialog, 
    QLineEdit, 
    QFormLayout, 
    QDialogButtonBox,
    QComboBox
)

from ETools import ETools

class EditDialog(QDialog):
    def __init__(self, name, location, type_, url, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Entry")
        self.setObjectName("editEntryWindow")
        self.resize(400, 200)

        self.name_input = QLineEdit(name)
        self.location_input = QLineEdit(location)
        self.type_input = QComboBox()
        sup_types = []
        for stype in ETools.SupportedTypes:
            sup_types.append(stype.name)
        self.type_input.addItems(sup_types)
        self.type_input.setCurrentText(type_)
        self.url_input = QLineEdit(url)

        form_layout = QFormLayout()
        form_layout.addRow(ETools.Key_ColumnName,       self.name_input)
        form_layout.addRow(ETools.Key_ColumnLocation,   self.location_input)
        form_layout.addRow(ETools.Key_ColumnType,       self.type_input)
        form_layout.addRow(ETools.Key_ColumnURL,        self.url_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def get_data(self):
        return self.name_input.text(), self.location_input.text(), self.type_input.currentText(), self.url_input.text()