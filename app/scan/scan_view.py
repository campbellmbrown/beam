from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QTableView, QVBoxLayout, QWidget


class ScanView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._create_widgets()

        layout = QVBoxLayout()
        layout.addWidget(self.scan_button, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.table_view)
        self.setLayout(layout)

    def _create_widgets(self) -> None:
        table_view = QTableView()
        table_view.setAlternatingRowColors(True)
        table_view.setShowGrid(False)
        table_view.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        table_view.setSortingEnabled(True)
        self.table_view = table_view
        self.scan_button = QPushButton("Scan")
