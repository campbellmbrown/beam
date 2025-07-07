import argparse
import asyncio
import time

from bleak import BleakClient

NEGOTATION_DELAY_S = 2.0


async def run(address: str) -> None:
    print(f"Connecting to {address}...")
    start_time = time.time()
    async with BleakClient(address) as client:
        if not client.is_connected:
            print("Failed to connect.")
            return
        print(f"Connected successfully in {time.time() - start_time:.2f} seconds.")
        print("Address:", client.address)

        print("Services:")
        for service in client.services:
            print(f"- [{service.handle}] {service.description} ({service.uuid})")
            if len(service.characteristics) > 0:
                print("  Characteristics:")
                for characteristic in service.characteristics:
                    print(
                        f"  - [{characteristic.handle}] {characteristic.description} ({characteristic.uuid}) "
                        + f"[{', '.join(characteristic.properties)}]"
                    )

        print("Waiting for MTU negotiation to complete...")
        await asyncio.sleep(NEGOTATION_DELAY_S)  # Small delay for negotiation
        print("MTU:", client.mtu_size)

        print("Disconnecting...")
        await client.disconnect()
        print("Done")


parser = argparse.ArgumentParser(description="Connect and probe a BLE peripheral device for information.")
parser.add_argument("address", help="The MAC address of the peripheral device.")
args = parser.parse_args()

asyncio.run(run(args.address))
