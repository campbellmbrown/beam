import argparse
import asyncio
import logging
from datetime import datetime

from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from bleak.exc import BleakDeviceNotFoundError

from core.device_registry import resolve_address


class AdvertistementScanner:
    def __init__(self, save_to_file: bool, address: str) -> None:
        self.save_to_file = save_to_file
        self.address = address

        self.save_file = datetime.now().strftime("advertisements_%Y%m%d_%H%M%S.csv")
        if self.save_to_file:
            logging.info("Saving advertisements to %s", self.save_file)
            with open(self.save_file, "w", encoding="utf-8") as f:
                f.write("timestamp,address,name,rssi\n")

    async def run(self) -> None:
        scanner = BleakScanner(self._detection_callback)
        logging.info("Scanning for advertisements from %s...", self.address)
        await scanner.start()
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logging.info("Stopping scan...")
        finally:
            await scanner.stop()

    def _detection_callback(self, device: BLEDevice, advertisement_data: AdvertisementData) -> None:
        if device.address == self.address:
            logging.info("%s name=%s, RSSI=%d", device.address, device.name, advertisement_data.rssi)
            if self.save_to_file:
                with open(self.save_file, "a", encoding="utf-8") as f:
                    timestamp = datetime.now().isoformat()
                    f.write(f"{timestamp},{device.address},{device.name},{advertisement_data.rssi}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan for BLE advertisements from a specific device.")
    parser.add_argument("target", help="MAC address or device ID")
    parser.add_argument("--save", action="store_true", help="Save advertisements to a CSV file")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    address = resolve_address(args.target)

    scanner = AdvertistementScanner(save_to_file=args.save, address=address)
    try:
        asyncio.run(scanner.run())
    except KeyboardInterrupt:
        print("Exiting...")
    except BleakDeviceNotFoundError:
        print(f"Device with address '{address}' not found.")
