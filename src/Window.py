import sys
from PySide6.QtWidgets import (
    QApplication, 
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout,
    QPushButton, 
    QTableWidget, 
    QTableWidgetItem, 
    QCheckBox, 
    QHeaderView, 
    QAbstractItemView, 
    QDialog 
)
from PySide6.QtCore import Qt
from EditWindow import EditDialog
from ETools import ETools

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("External Assets")
        self.resize(600, 400)

        main_layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["", "Name", "Location", "Type", "URL"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        db_data = ETools.load_json()
        if db_data is not None:
            for array_item in db_data:
                name        = array_item["name"]
                location    = array_item["location"]
                type_       = array_item["type"]
                url         = array_item["url"]

                self.add_table_item(False, name, location, type_, url)


        self.table.cellDoubleClicked.connect(self.open_edit_dialog)

        main_layout.addWidget(self.table)

        button_layout = QHBoxLayout()
        
        delete_button = QPushButton("Delete")
        add_button = QPushButton("Add")
        run_button = QPushButton("Run")

        add_button.clicked.connect(self.add_new_row)
        delete_button.clicked.connect(self.delete_selected_row)
        
        button_layout.addStretch(1)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(add_button)
        button_layout.addWidget(run_button)

        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
    
    @staticmethod
    def show_window():
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())

    def add_table_item(self, status, name, location, type_, url):
        checkbox = QCheckBox()
        checkbox.checkState = status
        checkbox_widget = QWidget()
        checkbox_layout = QHBoxLayout(checkbox_widget)
        checkbox_layout.addWidget(checkbox)
        checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        checkbox_layout.setContentsMargins(0, 0, 0, 0)
        
        row = self.table.rowCount()
        self.table.insertRow(row)

        self.table.setCellWidget(row, 0, checkbox_widget)
        self.table.setItem(row, 1, QTableWidgetItem(name))
        self.table.setItem(row, 2, QTableWidgetItem(location))
        self.table.setItem(row, 3, QTableWidgetItem(type_))
        self.table.setItem(row, 4, QTableWidgetItem(url))
    
    def open_edit_dialog(self, row, column):
        name        = self.table.item(row, 1).text()
        location    = self.table.item(row, 2).text()
        type_       = self.table.item(row, 3).text()
        url         = self.table.item(row, 4).text()

        dialog = EditDialog(name, location, type_, url, self)
        if dialog.exec() == QDialog.Accepted:
            name, location, type_, url = dialog.get_data()

            self.table.item(row, 1).setText(name)
            self.table.item(row, 2).setText(location)
            self.table.item(row, 3).setText(type_)
            self.table.item(row, 4).setText(url)
            
            self.save_data()
    
    def add_new_row(self):
        self.add_table_item(False, "", "", "", "")

    def delete_selected_row(self):
        current_row = self.table.currentRow()
        if current_row != -1:
            self.table.removeRow(current_row)

    def save_data(self):
        data = []
        for row in range(self.table.rowCount()):
            item_data = {
                "name":     self.table.item(row, 1).text(),
                "location": self.table.item(row, 2).text(),
                "type":     self.table.item(row, 3).text(),
                "url":      self.table.item(row, 4).text()
            }
            data.append(item_data)
        
        ETools.save_json(data)