from dataclasses import dataclass


@dataclass
class ScanItem:
    name: str
    mac_addr: str
