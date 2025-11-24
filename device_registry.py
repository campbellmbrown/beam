from pathlib import Path

import yaml


class DeviceRegistry:
    def __init__(self, yaml_file: Path | None) -> None:
        self.yaml_file = yaml_file
        self.devices: list[dict[str, str]] = []
        if self.yaml_file and self.yaml_file.exists():
            with open(self.yaml_file, encoding="utf-8") as file:
                loaded_registry = yaml.safe_load(file)
                self.devices = loaded_registry.get("devices", [])

        print(self.devices)

    def get_address(self, device_id: str) -> str | None:
        for device in self.devices:
            if device.get("id") == device_id:
                address = device.get("address")
                if address:
                    return address
        return None
