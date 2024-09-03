from typing import Dict, Optional

from ..Utils.Identity import Identity
from .Device import Device
from ..Config import CERROR_MESSAGES, CCAPABILITIES
from .Sensor import Sensor
from .Actuator import Actuator
from ..Models.MicrocontrollerCapabilities import MicroControllerCapabilities

class MicroController:

    _identity: str
    _description: str
    _devices: Dict[str, Device]
    _capabilities: MicroControllerCapabilities
    #TODO: networkinterface here for communication?!

    def __init__(self, identity: str, description: str = "") -> None:
        Identity.register(identity=identity)
        self._identity = identity
        self._description = description

        self._devices = {}
        self._capabilities = MicroControllerCapabilities(
            include_timestamp=CCAPABILITIES.DEFAULT_INCLUDE_TIMESTAMP,
            include_sequence=CCAPABILITIES.DEFAULT_INCLUDE_SEQUENCE,
            delay=CCAPABILITIES.DEFAULT_DELAY,
            duration=CCAPABILITIES.DEFAULT_DURATION,
            max_samples=CCAPABILITIES.DEFAULT_MAX_SAMPLES
        )#type: ignore

    def add_devices(self, *devices: Device) -> None:
        for device in devices:
            if not isinstance(device, (Sensor, Actuator)):
                raise TypeError(CERROR_MESSAGES.ALL_ARGUMENTS_DEVICE)

            if device.identity not in self._devices:
                self._devices[device.identity] = device


    def get_device(self, identity: str) -> Optional[Device]:
        #do not have to check if identity is in _devices because it automatically returns None if no device is found
        return self._devices.get(identity)

        

""" 
    def set_data(self, data: dict) -> None:
        for key, sensor_data in data.items():
            if key not in self.sensors:
                continue
            self.sensors[key].set_data(sensor_data)

    def get_data(self) -> dict[str, Sensor]:
        l = {}

        for identity, sensor in self.sensors.items():
            l[identity] = sensor.get_data()

        return l
    
    def _restart(self) -> None:
        raise NotImplementedError
    #restart the MC; only for GUI/CLI

    def _heartbeat(self) -> None:
        raise NotImplementedError
    #request a heartbeat from the microcontroller

    def _battery(self) -> None:
        raise NotImplementedError
    #request battery status from the MC

    def _get_capabilities(self) -> None:
        raise NotImplementedError
    #request on MC what capabilities are available

 """