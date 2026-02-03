import sys
from pathlib import Path
from typing import Callable

from PySide6.QtCore import Qt, QThread, Signal
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
    QLabel,
)
from PySide6 import QtGui

from config import AssetEntry, load_config, save_config
from sync_runner import SyncRunner
from edit_dialog import EditDialog


# ── worker thread ─────────────────────────────────────────────────────
# SyncRunner is CPU/IO-bound; run it off the main thread so the log pane
# stays responsive during downloads.

class _SyncWorker(QThread):
    log_line = Signal(str)          # emitted per log line
    finished = Signal()             # emitted when all entries are done

    def __init__(self, runner: SyncRunner, entries: list[AssetEntry]):
        super().__init__()
        self._runner  = runner
        self._entries = entries

    def run(self):
        self._runner.run(self._entries)
        self.finished.emit()


# ── main window ───────────────────────────────────────────────────────

class MainWindow(QWidget):

    def __init__(self, root_dir: Path, config_dir: Path):
        super().__init__()
        self._root_dir   = root_dir
        self._config_dir = config_dir
        self._temp_dir   = config_dir / "Temp"
        self._worker: _SyncWorker | None = None

        self.setWindowTitle("AssetPull")
        self.setObjectName("mainWindow")
        self.resize(1024, 700)

        self._build_ui()
        self._apply_styles()
        self._connect_signals()
        self._load_table()

    # ── UI construction ─────────────────────────────────────────────

    def _build_ui(self):
        main = QVBoxLayout()

        # ── asset table ─────────────────────────────────────────────
        self._table = QTableWidget()
        self._table.setColumnCount(5)
        self._table.setHorizontalHeaderLabels(["", "Name", "Location", "Type", "URL"])
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.horizontalHeader().setMinimumHeight(40)
        self._table.verticalHeader().setVisible(False)
        self._table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._table.setSelectionMode(QAbstractItemView.SingleSelection)
        self._table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        main.addWidget(self._table)

        # ── buttons ─────────────────────────────────────────────────
        btn_row = QHBoxLayout()
        self._btn_select_all = QPushButton("Select All")
        self._btn_none       = QPushButton("None")
        self._btn_delete     = QPushButton("Delete")
        self._btn_add        = QPushButton("Add")
        self._btn_run        = QPushButton("Sync")

        btn_row.addWidget(self._btn_select_all)
        btn_row.addWidget(self._btn_none)
        btn_row.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding))
        btn_row.addWidget(self._btn_delete)
        btn_row.addWidget(self._btn_add)
        btn_row.addWidget(self._btn_run)
        main.addLayout(btn_row)

        # ── log pane ────────────────────────────────────────────────
        main.addWidget(QLabel("Log"))
        self._log = QTextEdit()
        self._log.setReadOnly(True)
        main.addWidget(self._log)

        self.setLayout(main)

    def _connect_signals(self):
        self._table.cellDoubleClicked.connect(self._on_double_click)
        self._btn_add.clicked.connect(self._on_add)
        self._btn_delete.clicked.connect(self._on_delete)
        self._btn_select_all.clicked.connect(self._on_select_all)
        self._btn_none.clicked.connect(self._on_deselect_all)
        self._btn_run.clicked.connect(self._on_sync)

    # ── table helpers ───────────────────────────────────────────────

    def _load_table(self):
        self._table.setRowCount(0)
        for entry in load_config(self._config_dir):
            self._append_row(entry)

    def _append_row(self, entry: AssetEntry, checked: bool = False):
        row = self._table.rowCount()
        self._table.insertRow(row)

        # checkbox cell
        cb = QCheckBox()
        cb.setChecked(checked)
        wrapper = QWidget()
        layout  = QHBoxLayout(wrapper)
        layout.addWidget(cb)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        self._table.setCellWidget(row, 0, wrapper)

        # data cells
        for col, value in enumerate([entry.name, entry.location, entry.type, entry.url], start=1):
            self._table.setItem(row, col, QTableWidgetItem(value))

        self._table.setRowHeight(row, 44)

        # alternating row color
        bg = "#1E1E1E" if row % 2 else "#121212"
        wrapper.setStyleSheet(f"background-color: {bg};")
        for col in range(1, 5):
            self._table.item(row, col).setBackground(QtGui.QColor(bg))

    def _row_to_entry(self, row: int) -> AssetEntry:
        return AssetEntry(
            name=self._table.item(row, 1).text(),
            location=self._table.item(row, 2).text(),
            type=self._table.item(row, 3).text(),
            url=self._table.item(row, 4).text(),
        )

    def _save_table(self):
        entries = [self._row_to_entry(r) for r in range(self._table.rowCount())]
        save_config(self._config_dir, entries)

    # ── button handlers ─────────────────────────────────────────────

    def _on_double_click(self, row: int, _col: int):
        dialog = EditDialog(entry=self._row_to_entry(row), parent=self)
        if dialog.exec() == QDialog.Accepted:
            updated = dialog.get_entry()
            for col, val in enumerate([updated.name, updated.location, updated.type, updated.url], start=1):
                self._table.item(row, col).setText(val)
            self._save_table()

    def _on_add(self):
        dialog = EditDialog(parent=self)
        if dialog.exec() == QDialog.Accepted:
            self._append_row(dialog.get_entry())
            self._save_table()

    def _on_delete(self):
        row = self._table.currentRow()
        if row != -1:
            self._table.removeRow(row)
            self._save_table()

    def _on_select_all(self):
        self._set_all_checkboxes(True)

    def _on_deselect_all(self):
        self._set_all_checkboxes(False)

    def _set_all_checkboxes(self, state: bool):
        for row in range(self._table.rowCount()):
            cb = self._table.cellWidget(row, 0).layout().itemAt(0).widget()
            cb.setChecked(state)

    # ── sync ────────────────────────────────────────────────────────

    def _on_sync(self):
        selected = []
        for row in range(self._table.rowCount()):
            cb = self._table.cellWidget(row, 0).layout().itemAt(0).widget()
            if cb.isChecked():
                selected.append(self._row_to_entry(row))

        if not selected:
            self._write_log("Nothing selected.")
            return

        self._btn_run.setEnabled(False)
        runner = SyncRunner(self._root_dir, self._temp_dir, self._write_log)
        self._worker = _SyncWorker(runner, selected)
        self._worker.finished.connect(self._on_sync_finished)
        self._worker.start()

    def _on_sync_finished(self):
        self._btn_run.setEnabled(True)

    # ── log ─────────────────────────────────────────────────────────

    def _write_log(self, text: str):
        self._log.append(text)
        self._log.ensureCursorVisible()

    # ── styles ──────────────────────────────────────────────────────

    def _apply_styles(self):
        self.setStyleSheet("""
            QWidget#mainWindow, QDialog#editDialog {
            background-color: #0F1115; /* base */
        }

        QLabel {
            color: #E6EAF2;
            font-size: 13px;
            padding: 4px 0;
        }

        /* Inputs */
        QLineEdit, QComboBox, QTextEdit {
            background-color: #141823;      /* surface */
            color: #E6EAF2;
            border: 1px solid #232A3A;      /* subtle border */
            border-radius: 8px;
            padding: 8px 10px;
            font-size: 13px;
        }
        QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
            border: 1px solid #6D7CFF;      /* accent */
        }

        QComboBox::drop-down {
            border-left: 1px solid #232A3A;
            width: 28px;
        }
        QComboBox QAbstractItemView {
            background-color: #141823;
            color: #E6EAF2;
            border: 1px solid #232A3A;
            selection-background-color: #2A3350;
            selection-color: #E6EAF2;
        }

        /* Buttons – default */
        QPushButton {
            background-color: #1B2130; /* neutral */
            color: #E6EAF2;
            border: 1px solid #232A3A;
            border-radius: 10px;
            padding: 7px 14px;
            font-weight: 600;
        }
        QPushButton:hover {
            background-color: #222A3D;
            border: 1px solid #2B3550;
        }
        QPushButton:pressed {
            background-color: #161B27;
        }
        QPushButton:disabled {
            background-color: #121521;
            color: #6E768A;
            border: 1px solid #1B2030;
        }

        /* Primary / Danger via objectName */
        QPushButton#btnPrimary {
            background-color: #6D7CFF;  /* indigo */
            color: #0B0D12;
            border: none;
        }
        QPushButton#btnPrimary:hover   { background-color: #7D8BFF; }
        QPushButton#btnPrimary:pressed { background-color: #5D6CFF; }

        QPushButton#btnDanger {
            background-color: #2A1B1E;
            color: #FFB4BD;
            border: 1px solid #4A2A32;
        }
        QPushButton#btnDanger:hover {
            background-color: #351F24;
            border: 1px solid #5B2F39;
        }
        QPushButton#btnDanger:pressed {
            background-color: #24161A;
        }

        QPushButton#btnSecondary {
            background-color: #1B2130;
            color: #E6EAF2;
            border: 1px solid #232A3A;
        }

        /* Table */
        QTableWidget {
            border: 1px solid #1B2030;
            background-color: #0F1115;
            color: #E6EAF2;
            gridline-color: #0F1115;
            border-radius: 10px;
        }
        QHeaderView::section {
            background-color: #121521;
            color: #CFE0FF;
            padding: 8px;
            border: none;
            font-weight: 700;
        }
        QTableWidget::item {
            padding-left: 10px;
        }
        QTableWidget::item:selected {
            background-color: #2A3350;
            color: #E6EAF2;
        }

        /* Checkbox */
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
            border-radius: 5px;
        }
        QCheckBox::indicator:unchecked {
            border: 2px solid #2B3550;
            background-color: #141823;
        }
        QCheckBox::indicator:checked {
            border: 2px solid #6D7CFF;
            background-color: #6D7CFF;
        }

        /* Log */
        QTextEdit {
            font-family: "Consolas", "Courier New", monospace;
        }
        """)

    # ── static entry point ──────────────────────────────────────────

    @staticmethod
    def show_window(root_dir: Path, config_dir: Path):
        app = QApplication(sys.argv)
        window = MainWindow(root_dir, config_dir)
        window.show()
        sys.exit(app.exec())
