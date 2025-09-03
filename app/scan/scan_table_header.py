from enum import IntEnum


class ScanTableHeader(IntEnum):
    NAME = 0
    MAC_ADDR = 1
    RSSI = 2

    def to_str(self) -> str:
        return self.name.capitalize()
