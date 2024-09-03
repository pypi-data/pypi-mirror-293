from bleak import BleakScanner
from typing import List

from ..Models.BLEInfo import BLEInfo
from ..Config import CERROR_MESSAGES

async def scan_ble_addresses(device_names: List[str], timeout: int = 5) -> List[BLEInfo]:
    """
    This function scans for devices that are advertising their BLE presence. The function is an async function using asyncio. Therefore the function asyncio.run(scan_ble_addresses(["test-device"])) must be used to correctly invoke this function. It first checks if the device_names are of type list, even if it is only one item to void problems with the check if the device name is in the list. BleakScanner scans for all devices with BLE returning device and advertisement informations without in timeout window of 5 seconds per default. this can be adjusted. if the device matches one of the device_names - or partly - it is appended the list of devices that we are looking for. the BLEinfor class is a dataclass which contains the information about the mac address, the name of the device (usually a human readable string) and the service uuids - this is also a list because BLE servers can have multiple services.

    Source:
        https://github.com/hbldh/bleak
        https://github.com/hbldh/bleak/blob/develop/examples/discover.py

    Args:
        device_names (List[str]):
            list of ble device names. the name must not be complete (it checks if any part of the device name matches one of the lists items) although this can lead to unwated ble devices in the list.
        timeout (int):
            the BLE scanner stops after x seconds (5 seconds per default) and returns the list of ble devices found

    Returns:
        list of ble devices which match the device names list
    
    Raises:
        TypeError: if the argument device_names is not of type list
    """
    if type(device_names) != list:
        raise TypeError(CERROR_MESSAGES.TYPE_MUST_BE_LIST)
    
    ble_addresses: List[BLEInfo] = []

    devices = await BleakScanner.discover(return_adv=True, timeout=timeout)

    for device, adv in devices.values():
        if any(keyword in device.name for keyword in device_names):
            ble_addresses.append(BLEInfo(address=device.address, name=device.name, service_uuids=adv.service_uuids))
  
    return ble_addresses
