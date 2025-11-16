# BEAM

BEAM - BLE Easy-Access Manager

## Usage

### Device Registry

You can create a device registry to avoid having to remember MAC addresses. Create a `registry.yaml` file in the same directory as the script with the following format:

```yaml
devices:
  - id: my_device
    address: 12:34:56:78:9A:BC
  - id: another_device
    address: 98:76:54:32:10:FE
```

Then use the device ID as the `target` argument when running a script.
If the `registry.yaml` doesn't exist, if the `registry.yaml` fails to load, or if the provided target is not found in the register, the script will fall back to using the provided target as the address directly.
