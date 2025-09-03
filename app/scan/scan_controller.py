from PySide6.QtWidgets import QHeaderView

from app.scan.scan_table_adapter import ScanTableAdapter
from app.scan.scan_table_header import ScanTableHeader
from app.scan.scan_view import ScanView


class ScanController:
    def __init__(self, view: ScanView) -> None:
        view.scan_button.clicked.connect(self._on_scan)

        # Adapter to handle data for the table view
        self.table_adapter = ScanTableAdapter()

        view.table_view.setModel(self.table_adapter)
        header = view.table_view.horizontalHeader()
        assert isinstance(header, QHeaderView)
        header.setSectionResizeMode(ScanTableHeader.NAME, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(ScanTableHeader.MAC_ADDR, QHeaderView.ResizeMode.Stretch)

    def _on_scan(self) -> None:
        pass
