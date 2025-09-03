from PySide6.QtBluetooth import QBluetoothDeviceDiscoveryAgent, QBluetoothDeviceInfo
from PySide6.QtCore import QObject, Signal


class ScanModel(QObject):
    device_discovered = Signal(QBluetoothDeviceInfo)
    device_updated = Signal(QBluetoothDeviceInfo, QBluetoothDeviceInfo.Field)

    def __init__(self) -> None:
        super().__init__()

        self.agent = QBluetoothDeviceDiscoveryAgent()
        self.agent.deviceDiscovered.connect(self._on_device_discovered)
        self.agent.deviceUpdated.connect(self._on_device_updated)
        self.agent.errorOccurred.connect(self._on_scan_error)
        self.agent.canceled.connect(self._on_scan_canceled)
        self.agent.finished.connect(self._on_scan_finished)

    def start(self, scan_duration: float = 10.0) -> None:
        if self.agent.isActive():
            return

        self.agent.setLowEnergyDiscoveryTimeout(int(scan_duration * 1000))
        self.agent.start(QBluetoothDeviceDiscoveryAgent.DiscoveryMethod.LowEnergyMethod)

    def _on_device_discovered(self, device: QBluetoothDeviceInfo) -> None:
        print(f"Discovered device: {device.name()} ({device.address().toString()})")
        assert device.coreConfigurations() & QBluetoothDeviceInfo.CoreConfiguration.LowEnergyCoreConfiguration
        self.device_discovered.emit(device)

    def _on_device_updated(self, device: QBluetoothDeviceInfo, updated_fields: QBluetoothDeviceInfo.Field) -> None:
        print(f"Updated device: {device.address().toString()}: {updated_fields}")
        self.device_updated.emit(device, updated_fields)

    def _on_scan_error(self, error: QBluetoothDeviceDiscoveryAgent.Error) -> None:
        print(f"Bluetooth scan error occurred: {error}")

    def _on_scan_canceled(self) -> None:
        print("Bluetooth scan canceled")

    def _on_scan_finished(self) -> None:
        print("Bluetooth scan finished")
