# BEAM - BLE Easy-Access Manager

![License](https://img.shields.io/github/license/campbellmbrown/beam)
![Release](https://img.shields.io/github/v/release/campbellmbrown/beam)
![Contributors](https://img.shields.io/github/contributors/campbellmbrown/beam)
![Issues](https://img.shields.io/github/issues/campbellmbrown/beam)
![Pull Requests](https://img.shields.io/github/issues-pr/campbellmbrown/beam)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

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
