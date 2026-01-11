import argparse
import asyncio
import logging
import time

from bleak import BleakClient

NEGOTIATION_DELAY_S = 2.0


async def run(address: str) -> None:
    logging.info("Connecting to %s...", address)
    start_time = time.time()
    async with BleakClient(address) as client:
        if not client.is_connected:
            logging.error("Failed to connect.")
            return
        logging.info("Connected successfully in %.2f seconds.", time.time() - start_time)
        logging.info("Address: %s", client.address)

        logging.info("Services:")
        for service in client.services:
            logging.info("- [%d] %s (%s)", service.handle, service.description, service.uuid)
            if len(service.characteristics) > 0:
                logging.info("  Characteristics:")
                for characteristic in service.characteristics:
                    logging.info(
                        "  - [%d] %s (%s) [%s]",
                        characteristic.handle,
                        characteristic.description,
                        characteristic.uuid,
                        ", ".join(characteristic.properties),
                    )

        logging.info("Waiting for MTU negotiation to complete...")
        await asyncio.sleep(NEGOTIATION_DELAY_S)  # Small delay for negotiation
        logging.info("MTU: %d", client.mtu_size)

        logging.info("Disconnecting...")
        await client.disconnect()
        logging.info("Done")


parser = argparse.ArgumentParser(description="Connect and probe a BLE peripheral device for information.")
parser.add_argument("address", help="The MAC address of the peripheral device.")
args = parser.parse_args()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

asyncio.run(run(args.address))
