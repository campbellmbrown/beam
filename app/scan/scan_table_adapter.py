from typing import Any, Union

from PySide6.QtCore import QAbstractTableModel, QModelIndex, QPersistentModelIndex, Qt
from PySide6.QtGui import QColor

from app.scan.scan_item import ScanItem
from app.scan.scan_table_header import ScanTableHeader

ModelIndex = Union[QModelIndex, QPersistentModelIndex]


class ScanTableAdapter(QAbstractTableModel):
    def __init__(self) -> None:
        super().__init__()
        self.items: dict[str, ScanItem] = {}

    def add_item(self, item: ScanItem) -> None:
        """
        Add an item to the end of the table.
        """
        assert item.mac_addr not in self.items
        row = len(self.items)

        # This must be called before inserting data into the underlying data store
        self.beginInsertRows(QModelIndex(), row, row)
        self.items[item.mac_addr] = item
        self.endInsertRows()

        # Notify the view that the data has changed
        top_left = self.index(row, 0)
        bottom_right = self.index(row, len(ScanTableHeader) - 1)
        self.dataChanged.emit(top_left, bottom_right)

    def update_item(self, item: ScanItem) -> None:
        assert item.mac_addr in self.items
        self.items[item.mac_addr] = item

        row = list(self.items.keys()).index(item.mac_addr)
        top_left = self.index(row, 0)
        bottom_right = self.index(row, len(ScanTableHeader) - 1)
        self.dataChanged.emit(top_left, bottom_right)

    def clear(self) -> None:
        """
        Clear the table and remove all items.
        """
        self.beginResetModel()
        self.items.clear()
        self.endResetModel()

    # We are overriding the base class (library) function, so we can't change the signature.
    def rowCount(self, parent: ModelIndex = QModelIndex()) -> int:  # noqa: B008
        """
        Implements the base abstract method to provide the number of rows in the table.
        """
        return len(self.items)

    # We are overriding the base class (library) function, so we can't change the signature.
    def columnCount(self, parent: ModelIndex = QModelIndex()) -> int:  # noqa: B008
        """
        Implements the base abstract method to provide the number of columns in the table.
        """
        return len(ScanTableHeader)

    def data(self, index: ModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        """
        Implements the base abstract method to provide the data for each item in the table.
        """

        if not index.isValid():
            return None

        row = index.row()
        col = index.column()

        # The DisplayRole is used to display the data in the table.
        # The UserRole is used to provide additional data for the item, e.g. for sorting/filtering.
        # The EditRole is used to provide initial data when editing the item.
        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.UserRole, Qt.ItemDataRole.EditRole):
            if col == ScanTableHeader.NAME:
                return list(self.items.values())[row].name
            if col == ScanTableHeader.MAC_ADDR:
                return list(self.items.values())[row].mac_addr
            if col == ScanTableHeader.RSSI:
                return list(self.items.values())[row].rssi
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        """
        Implements the base abstract method to provide the header data for the table.
        """
        if orientation == Qt.Orientation.Vertical:
            # Only the horizontal header is used
            return None

        # Provide text for the header
        if role == Qt.ItemDataRole.DisplayRole:
            return ScanTableHeader(section).to_str()

        # Appearance of the header
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        if role == Qt.ItemDataRole.ForegroundRole:
            return QColor(Qt.GlobalColor.gray)

        return None

    def flags(self, index: ModelIndex) -> Qt.ItemFlag:
        """
        Provides flags for each item in the table.
        """
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags

        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
