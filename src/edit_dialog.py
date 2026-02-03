from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QDialogButtonBox,
)

from config import AssetEntry
from provider_registry import available_types


class EditDialog(QDialog):
    """Modal dialog for creating or editing a single AssetEntry."""

    def __init__(self, entry: AssetEntry | None = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Asset" if entry else "Add Asset")
        self.setObjectName("editDialog")
        self.setMinimumWidth(440)

        # ── inputs ──────────────────────────────────────────────────
        self._name     = QLineEdit(entry.name     if entry else "")
        self._location = QLineEdit(entry.location if entry else "")
        self._url      = QLineEdit(entry.url      if entry else "")

        self._type = QComboBox()
        self._type.addItems(available_types())
        if entry:
            self._type.setCurrentText(entry.type)

        # ── layout ──────────────────────────────────────────────────
        form = QFormLayout()
        form.addRow("Name",     self._name)
        form.addRow("Location", self._location)
        form.addRow("Type",     self._type)
        form.addRow("URL",      self._url)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(buttons)
        self.setLayout(layout)

    # ── public ──────────────────────────────────────────────────────

    def get_entry(self) -> AssetEntry:
        """Read current form state as an AssetEntry."""
        return AssetEntry(
            name=self._name.text().strip(),
            location=self._location.text().strip(),
            type=self._type.currentText(),
            url=self._url.text().strip(),
        )
