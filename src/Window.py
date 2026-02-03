import sys
from ETools import ETools
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
    QTextEdit,
    QLabel
)
from PySide6 import QtGui

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Externals Tool")
        self.resize(1024, 768)

        self.setup_ui()
        self.setup_callbacks()
        self.setup_styles()
        self.fill_table_from_file()

        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.table.horizontalHeader().setMinimumHeight(50)
        self.table.verticalHeader().setVisible(False)

        self.controll = CommandControll()
    
    def setup_ui(self):

        self.setWindowIcon(QtGui.QIcon(ETools.get_execution_path() + "\\..\\Resources\\logo.ico"))
        
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

        console_text = QLabel()
        console_text.setText("Log output")
        main_layout.addWidget(console_text)

        # process log
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        main_layout.addWidget(self.console)
        
        self.setLayout(main_layout)
    
    def setup_styles(self):
        self.setObjectName("mainWindow")
        self.setStyleSheet("""
            QWidget#mainWindow, QDialog#editEntryWindow {
                background-color: #121212;
            }
            
            QLabel {
                color: #f0f0f0;
            }               
            
            QPushButton {
                background-color: #03DAC6;
                color: #000000;
                border: 1px solid #03DAC6;
                border-radius: 5px;
                padding: 5px 15px 5px 15px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            QPushButton:pressed {
                background-color: #a0a0a0;
            }
            
            QTableWidget {
                border: none;
                background-color: #121212;
                color: #f0f0f0;
                gridline-color: #121212;
            }
            QHeaderView::section {
                background-color: #191919;
                color: #f0f0f0;
                padding: 5px;
                border: 1px solid #191919;
                font-weight: bold;
            }
            QTableCornerButton::section {
                background-color: #191919;
                border: 1px solid #191919;
            }
            QTableWidget::item:selected {
                background-color: #555555;
                color: #ffffff;
            }
                           
            QScrollBar:vertical {
                border-radius: 5px;
                background: #1E1E1E;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #03DAC6;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            
            QCheckBox {
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
                border-radius: 5px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #555555;
                background-color: #2e2e2e;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #03DAC6;
                background-color: #03DAC6;
            }
            QCheckBox::indicator:unchecked:hover {
                border: 2px solid #777777;
                background-color: #3e3e3e;
            }
            QCheckBox::indicator:checked:hover {
                border: 2px solid #03DAC6;
                background-color: #aaaaaa;
            }
            QCheckBox::indicator:unchecked:pressed {
                border: 2px solid #aaaaaa;
                background-color: #555555;
            }
            QCheckBox::indicator:checked:pressed {
                border: 2px solid #03DAC6;
                background-color: #aaaaaa;
            }
                           
            QTextEdit {
                background-color: #1E1E1E;
                color: #f0f0f0;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-family: "Arial";
            }
                           
            QLineEdit {
                background-color: #1E1E1E;
                border: 1px solid #1E1E1E;
                color: #f0f0f0;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #777777;
            }
                           
            QComboBox {
                background-color: #1E1E1E;
                color: #f0f0f0;
                border: 1px solid #1E1E1E;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 14px;
            }
            QComboBox:focus {
                border: 1px solid #777777;
            }
            QComboBox::drop-down {
                border-radius: 5px;
                background-color: #2e2e2e;
            }
            QComboBox QAbstractItemView {
                background-color: #2e2e2e;
                color: #f0f0f0;
                selection-background-color: #444444;
                selection-color: #ffffff;
            }
            QComboBox::item {
                padding: 5px;
            }
        """)
    
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

        db_data = ETools.load_config()
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
        self.table.setRowHeight(row, 50)

        color = "#1E1E1E" if row % 2 != 0 else "#121212"
        for i in range(self.table.columnCount()):
            if i == 0:
                item = self.table.cellWidget(row, i)
                item.setStyleSheet(f"background-color: {color};")
            else:
                item = self.table.item(row, i)
                item.setBackground(QtGui.QColor(color))
    
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
        
        ETools.save_config(data)
    
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