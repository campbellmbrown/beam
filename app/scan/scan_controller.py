from PySide6.QtBluetooth import QBluetoothDeviceInfo
from PySide6.QtCore import QSortFilterProxyModel, Qt
from PySide6.QtWidgets import QHeaderView

from app.scan.scan_item import ScanItem
from app.scan.scan_model import ScanModel
from app.scan.scan_table_adapter import ScanTableAdapter
from app.scan.scan_table_header import ScanTableHeader
from app.scan.scan_view import ScanView


class ScanController:
    def __init__(self, view: ScanView, model: ScanModel) -> None:
        view.scan_button.clicked.connect(self._on_scan)
        self.model = model
        self.model.device_discovered.connect(self._on_device_discovered)
        self.model.device_updated.connect(self._on_device_updated)

        # Adapter to handle data for the table view
        self.table_adapter = ScanTableAdapter()

        proxy = QSortFilterProxyModel()
        proxy.setSourceModel(self.table_adapter)
        proxy.setSortCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

        view.table_view.setModel(proxy)
        header = view.table_view.horizontalHeader()
        assert isinstance(header, QHeaderView)
        header.setSectionResizeMode(ScanTableHeader.NAME, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(ScanTableHeader.MAC_ADDR, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(ScanTableHeader.RSSI, QHeaderView.ResizeMode.ResizeToContents)

    def _on_scan(self) -> None:
        self.table_adapter.clear()
        self.model.start()

    def _on_device_discovered(self, device: QBluetoothDeviceInfo) -> None:
        item = ScanItem(
            name=device.name(),
            mac_addr=device.address().toString(),
            rssi=device.rssi(),
        )
        self.table_adapter.add_item(item)

    def _on_device_updated(self, device: QBluetoothDeviceInfo, _updated_fields: QBluetoothDeviceInfo.Field) -> None:
        item = ScanItem(
            name=device.name(),
            mac_addr=device.address().toString(),
            rssi=device.rssi(),
        )
        self.table_adapter.update_item(item)
