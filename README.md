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
  - id: "my_device"
    address: "12:34:56:78:9A:BC"
  - id: "another_device"
    address: "98:76:54:32:10:FE"
```

Then use the device ID as the `target` argument when running a script.
If the `registry.yaml` doesn't exist, if the `registry.yaml` fails to load, or if the provided target is not found in the register, the script will fall back to using the provided target as the address directly.

### BLE Device Scanning

To scan for advertising BLE devices, run the following command:

```bash
python ble_scan.py [--duration <seconds>] [--ignore-no-name]
```

* `--duration`: Optional duration (in seconds) to run the scan. Default is 10 seconds.
* `--ignore-no-name`: Optional flag to ignore devices without a name.

Devices found during the scan will be displayed in a table format.
Skipped devices due to `--ignore-no-name` will not be shown (evident by gaps in the index).

Example output:

```
❯ python ble_scan.py --duration 5 --ignore-no-name
Scanning: 100%|██████████████████████████████████████████████████████████████████| 25/25 [00:05<00:00,  4.88s/s]
  Index  Address            Name                   RSSI Max    RSSI Min
-------  -----------------  -------------------  ----------  ----------
      0  94:A0:81:4F:AD:13  Device A                    -78         -81
      2  94:A0:81:4F:32:F1  Device B                    -77         -93
      3  56:AF:FC:B1:B2:9E  Device C                    -83         -83
```

### BLE Advertising Scanning

To scan for BLE advertisements from a specific device, run the following command:

```bash
python ble_advert_scan.py --target <device ID or address> [--save]
```

* `--target`: The device ID (from the registry) or the MAC address of the target device.
* `--save`: Optional flag to save the advertisements to a CSV file named `<address>_adverts.csv`.

If the `--save` flag is provided, advertisements will be saved to a CSV file named `advertisements_<timestamp>.csv`.

Example CSV content:
```
timestamp,address,name,rssi
2026-01-12T10:09:41.135536,94:A0:81:4F:AD:13,CW WIFI,-76
2026-01-12T10:09:41.137217,94:A0:81:4F:AD:13,CW WIFI,-76
2026-01-12T10:09:45.044471,94:A0:81:4F:AD:13,CW WIFI,-79
2026-01-12T10:09:45.045850,94:A0:81:4F:AD:13,CW WIFI,-77
2026-01-12T10:09:46.562906,94:A0:81:4F:AD:13,CW WIFI,-81
```
