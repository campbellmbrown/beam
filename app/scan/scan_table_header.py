from enum import IntEnum


class ScanTableHeader(IntEnum):
    NAME = 0
    MAC_ADDR = 1
    RSSI = 2

    def to_str(self) -> str:
        return HEADER_DISPLAY_NAMES[self]


HEADER_DISPLAY_NAMES = {
    ScanTableHeader.NAME: "Name",
    ScanTableHeader.MAC_ADDR: "MAC Address",
    ScanTableHeader.RSSI: "RSSI",
}
