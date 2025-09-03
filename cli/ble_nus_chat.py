import argparse
import asyncio
import time

from aioconsole import ainput
from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic

import nordic_uart_service as nus


class BleNusChat:
    def __init__(self, append_newline: bool = False) -> None:
        self.append_newline = append_newline
        self.client: BleakClient | None = None
        self.rx_characteristic: BleakGATTCharacteristic | None = None

    async def run(self, address: str) -> None:
        print(f"Connecting to {address}...")
        start_time = time.time()
        async with BleakClient(address) as client:
            self.client = client
            if not client.is_connected:
                print("Failed to connect.")
                return
            print(f"Connected successfully in {time.time() - start_time:.2f} seconds.")

            nus_service = client.services.get_service(nus.SERVICE_UUID)
            if nus_service is None:
                print("Nordic UART Service not found.")
                return

            rx_characteristic = nus_service.get_characteristic(nus.RX_CHARACTERISTIC_UUID)
            tx_characteristic = nus_service.get_characteristic(nus.TX_CHARACTERISTIC_UUID)
            if rx_characteristic is None or tx_characteristic is None:
                print("Nordic UART characteristics not found.")
                return
            self.rx_characteristic = rx_characteristic

            await client.start_notify(tx_characteristic, self._notification_handler)

            input_task = asyncio.create_task(self._input_handler())
            disconnect_task = asyncio.create_task(self._wait_for_disconnect())
            await asyncio.gather(input_task, disconnect_task)

    async def _input_handler(self) -> None:
        while True:
            tx_data = await ainput()
            if tx_data == "exit":
                break
            if self.append_newline:
                tx_data += "\n"
            assert self.client is not None
            assert self.rx_characteristic is not None
            await self.client.write_gatt_char(self.rx_characteristic, tx_data.encode("utf-8"))

    async def _wait_for_disconnect(self) -> None:
        assert self.client is not None
        while self.client.is_connected:
            await asyncio.sleep(1)

    def _notification_handler(self, _sender: BleakGATTCharacteristic, data: bytearray) -> None:
        print(data.decode(), end="")
        print(data.hex())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chat with a BLE device using the Nordic UART Service (NUS).")
    parser.add_argument("address", help="The MAC address of the peripheral device.")
    parser.add_argument(
        "-n", "--newline", action="store_true", help="Append a newline character to each message sent to the device."
    )
    args = parser.parse_args()

    ble_nus_chat = BleNusChat(append_newline=args.newline)
    try:
        asyncio.run(ble_nus_chat.run(args.address))
    except KeyboardInterrupt:
        print("Exiting...")
