from dataclasses import dataclass, asdict, field
from typing import Self, Dict, List
from ..Network.NetworkInterface import NetworkProtocols
from ..Models.WiFiProfile import WiFiProfile
from ..Devices.Sensor import Sensor
from ..Devices.Actuator import Actuator
from ..Models.Battery import Battery

@dataclass
class MicroControllerCapabilities:
    include_timestamp: bool
    include_sequence: bool
    delay: int
    duration: int
    max_samples: int

    #status
    online: bool
    wifi_key: str
    serial_port: str
    identity: str
    battery: Battery
    sensors: List[Sensor]
    actuators: List[Actuator]
    protocol: NetworkProtocols = field(default=NetworkProtocols.BLE)

    def format_string(self) -> str:
        return f"identity: {self.identity} -- protocol: {self.protocol} -- online: {self.online} -- serial port: {self.serial_port}"

    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> Self:
        default_data = {
            'include_timestamp': False,
            'include_sequence': False,
            'delay': 0,
            'duration': 0,
            'max_samples': 0,
            'online': False,
            'protocol': NetworkProtocols.BLE,  # or a default NetworkProtocols value if available
            'wifi_key': "",
            'serial_port': "",
            'identity': "",
            'battery': 0,
            'sensors': [],
            'actuators': []
        }
        # Merge the provided data with default values
        merged_data = {**default_data, **data}
        return cls(**merged_data)