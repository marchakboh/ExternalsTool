from PySide6.QtWidgets import (
    QVBoxLayout,
    QDialog, 
    QLineEdit, 
    QFormLayout, 
    QDialogButtonBox
)

class EditDialog(QDialog):
    def __init__(self, name, location, type_, url, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Entry")
        self.resize(400, 200)

        self.name_input = QLineEdit(name)
        self.location_input = QLineEdit(location)
        self.type_input = QLineEdit(type_)
        self.url_input = QLineEdit(url)

        form_layout = QFormLayout()
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Location:", self.location_input)
        form_layout.addRow("Type:", self.type_input)
        form_layout.addRow("URL:", self.url_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def get_data(self):
        return self.name_input.text(), self.location_input.text(), self.type_input.text(), self.url_input.text()