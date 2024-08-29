import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

import logging

from vconnex.api import VconnexAPI
from vconnex.device import (VconnexDevice, VconnexDeviceListener,
                            VconnexDeviceManager)

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger()


class DeviceListenter(VconnexDeviceListener):
    def on_device_update(
        self, new_device: VconnexDevice, old_device: VconnexDevice = None
    ):
        """Update device info."""
        _LOGGER.info(f"\ndevice_update: new={new_device}, old={old_device}")

    def on_device_added(self, device: VconnexDevice):
        """Device Added."""
        _LOGGER.info(f"\ndevice_add: device={device}")

    def on_device_removed(self, device: VconnexDevice):
        """Device removed."""
        _LOGGER.info(f"\ndevice_remove: device={device}")


END_POINT = "http://localhost:8201/hass-api"
CLIENT_ID = "1"
CLIENT_SECRET = "1"

api = VconnexAPI(END_POINT, CLIENT_ID, CLIENT_SECRET)
device_manager = VconnexDeviceManager(api)
device_manager.add_device_listener(DeviceListenter())
device_manager.add_device_data_listener(
    lambda device_id, msg_dict: _LOGGER.info(
        "\ndevice_id=%s, msg=%s", device_id, json.dumps(msg_dict)
    )
)


_LOGGER.info("\nPress:\n\t[i]: initialize\n\t[r]: reload\n\t[d]: release\n\t[q]: quit")
while True:
    c = sys.stdin.readline()[0]
    if c == "q":
        break
    elif c == "i":
        _LOGGER.info("initialize")
        device_manager.initialize()
    elif c == "r":
        _LOGGER.info("reload")
        device_manager.reload()
    elif c == "d":
        _LOGGER.info("release")
        device_manager.release()
    elif c != "\n":
        _LOGGER.info(f"unsuported [{c}]")
