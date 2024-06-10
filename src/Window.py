import sys
import ETools
from PySide6.QtCore import Qt
from EditWindow import EditDialog
from CommandControll import CommandControll
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
    QDialog,
    QSpacerItem,
    QSizePolicy,
    QTextEdit
)

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("External Assets")
        self.resize(600, 400)

        self.setup_ui()
        self.setup_callbacks()
        self.fill_table_from_file()

        self.controll = CommandControll()
    
    def setup_ui(self):
        
        main_layout = QVBoxLayout()

        # table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["", ETools.Key_ColumnName, ETools.Key_ColumnLocation, ETools.Key_ColumnType, ETools.Key_ColumnURL])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        main_layout.addWidget(self.table)

        # buttons
        button_layout           = QHBoxLayout()
        self.select_all_button  = QPushButton("Select All")
        self.none_button        = QPushButton("None")
        self.delete_button      = QPushButton("Delete")
        self.add_button         = QPushButton("Add")
        self.run_button         = QPushButton("Run")

        button_layout.addWidget(self.select_all_button)
        button_layout.addWidget(self.none_button)
        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.run_button)

        main_layout.addLayout(button_layout)

        # process log
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        main_layout.addWidget(self.console)
        
        self.setLayout(main_layout)
    
    def setup_callbacks(self):
        # table
        self.table.cellDoubleClicked.connect(self.open_edit_dialog)
        
        #buttons
        self.add_button.clicked.connect(self.add_new_row)
        self.delete_button.clicked.connect(self.delete_selected_row)
        self.select_all_button.clicked.connect(self.select_all)
        self.none_button.clicked.connect(self.deselect_all)
        self.run_button.clicked.connect(self.on_run_tool)
    
    def fill_table_from_file(self):
        # clear rows
        self.table.setRowCount(0)

        db_data = ETools.ETools.load_json()
        if db_data is not None:
            for array_item in db_data:
                name        = array_item[ETools.Key_ColumnName]
                location    = array_item[ETools.Key_ColumnLocation]
                type_       = array_item[ETools.Key_ColumnType]
                url         = array_item[ETools.Key_ColumnURL]

                self.add_table_item(False, name, location, type_, url)

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
            self.save_data()
    
    def select_all(self):
        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 0).layout().itemAt(0).widget()
            checkbox.setChecked(True)
    
    def deselect_all(self):
        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 0).layout().itemAt(0).widget()
            checkbox.setChecked(False)
    
    def save_data(self):
        data = []
        for row in range(self.table.rowCount()):
            item_data = {
                ETools.Key_ColumnName:      self.table.item(row, 1).text(),
                ETools.Key_ColumnLocation:  self.table.item(row, 2).text(),
                ETools.Key_ColumnType:      self.table.item(row, 3).text(),
                ETools.Key_ColumnURL:       self.table.item(row, 4).text()
            }
            data.append(item_data)
        
        ETools.ETools.save_json(data)
    
    def on_run_tool(self):
        array_data = []
        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 0).layout().itemAt(0).widget()
            if checkbox.isChecked():
                item_data = {
                    ETools.Key_ColumnName:      self.table.item(row, 1).text(),
                    ETools.Key_ColumnLocation:  self.table.item(row, 2).text(),
                    ETools.Key_ColumnType:      self.table.item(row, 3).text(),
                    ETools.Key_ColumnURL:       self.table.item(row, 4).text()
                }
                array_data.append(item_data)
        
        self.controll.run_process(array_data, self.on_process_log)

    def on_process_log(self, log_str):
        self.console.append(log_str)
        self.console.ensureCursorVisible()
    
    @staticmethod
    def show_window():
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())