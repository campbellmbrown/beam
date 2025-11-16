from pathlib import Path

import yaml


class DeviceRegistry:
    def __init__(self, yaml_file: Path | None) -> None:
        self.yaml_file = yaml_file
        self.devices = self._load_devices()

    def _load_devices(self) -> dict[str, str]:
        if not self.yaml_file or not self.yaml_file.exists():
            return {}
        with open(self.yaml_file, encoding="utf-8") as file:
            return yaml.safe_load(file) or {}

    def get_address(self, device_id: str) -> str | None:
        return self.devices.get(device_id)
