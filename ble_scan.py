import argparse
import asyncio
import logging

from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from tabulate import tabulate
from tqdm import tqdm

TIMER_RESOLUTION = 0.2  # seconds


class DiscoveredDevice:
    def __init__(self, device: BLEDevice, advertisement_data: AdvertisementData):
        self.address = device.address
        self.name = device.name
        self.advertisement_data = [advertisement_data]

    def new_advertisement_data(self, device: BLEDevice, advertisement_data: AdvertisementData) -> None:
        self.advertisement_data.append(advertisement_data)
        if self.name is None:
            self.name = device.name
        assert self.name == device.name  # The name should not change

    def rssis(self) -> list[int]:
        return [advertisement_data.rssi for advertisement_data in self.advertisement_data]


class BleScanner:
    def __init__(self, duration_s: int, ignore_no_name: bool):
        self.devices: list[DiscoveredDevice] = []
        self.duration_s = duration_s
        self.ignore_no_name = ignore_no_name

    async def run(self) -> None:
        scanner = BleakScanner(detection_callback=self._detection_callback)
        await scanner.start()

        for _ in tqdm(range(round(self.duration_s * (1 / TIMER_RESOLUTION))), desc="Scanning", unit="s"):
            await asyncio.sleep(TIMER_RESOLUTION)

        await scanner.stop()

        tabulated = [
            [
                idx,
                discovered_device.address,
                discovered_device.name or "-",
                max(discovered_device.rssis()),
                min(discovered_device.rssis()),
            ]
            for idx, discovered_device in enumerate(self.devices)
            if not self.ignore_no_name or discovered_device.name is not None
        ]
        print(tabulate(tabulated, headers=["Index", "Address", "Name", "RSSI Max", "RSSI Min"], tablefmt="simple"))

    def _detection_callback(self, device: BLEDevice, advertisement_data: AdvertisementData) -> None:
        for discovered_device in self.devices:
            if discovered_device.address == device.address:
                discovered_device.new_advertisement_data(device, advertisement_data)
                break
        else:
            discovered_device = DiscoveredDevice(device, advertisement_data)
            self.devices.append(discovered_device)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan for BLE devices.")
    parser.add_argument(
        "-d", "--duration", type=int, default=10, help="Duration in seconds to scan for. Default is 10."
    )
    parser.add_argument("-i", "--ignore-no-name", action="store_true", help="Ignore devices without a name.")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    ble_scanner = BleScanner(args.duration, args.ignore_no_name)
    asyncio.run(ble_scanner.run())
