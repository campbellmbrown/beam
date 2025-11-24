from pathlib import Path

import yaml


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
