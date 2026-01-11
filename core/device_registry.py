import logging
from pathlib import Path

import yaml

DEFAULT_REGISTRY = Path("registry.yaml")


class DeviceRegistry:
    def __init__(self, yaml_file: Path | None) -> None:
        self.devices: list[dict[str, str]] = []
        if yaml_file and yaml_file.exists():
            self.registry_exists = True
            with open(yaml_file, encoding="utf-8") as file:
                loaded_registry = yaml.safe_load(file)
                self.devices = loaded_registry.get("devices", [])

    def get_address(self, device_id: str) -> str | None:
        for device in self.devices:
            if device.get("id") == device_id:
                address = device.get("address")
                if address:
                    return address
        return None


def resolve_address(target: str) -> str:
    registry = DeviceRegistry(DEFAULT_REGISTRY)
    if registry.registry_exists:
        address_from_id = registry.get_address(target)
        if address_from_id is not None:
            logging.info("Resolved device ID '%s' to address '%s'.", target, address_from_id)
            address = address_from_id
        else:
            # Use the provided target as the address
            logging.info("Device ID '%s' not found in registry. Using provided target '%s' as address.", target, target)
            address = target
    else:
        logging.info("Device registry not found. Using provided target '%s' as address.", target)
        address = target

    return address
