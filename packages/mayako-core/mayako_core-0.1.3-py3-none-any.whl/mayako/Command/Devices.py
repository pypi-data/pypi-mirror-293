from .BaseCommand import BaseCommand, BaseCommandKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Devices.MicroController import MicroController
    from ..Devices.Sensor import Sensor
    from ..Devices.Actuator import Actuator

class MicrocontrollerRestart(BaseCommand):

    def __init__(self, microcontroller: MicroController) -> None:
        super().__init__()
        self.microcontroller = microcontroller

    def execute(self) -> None:
        self.microcontroller._restart()

class MicrocontrollerBatteryRead(BaseCommand):

    def __init__(self, microcontroller: MicroController) -> None:
        super().__init__()
        self.microcontroller = microcontroller

    def execute(self) -> None:
        self.microcontroller._battery_read()

class MicrocontrollerCapabilitiesRead(BaseCommand):

    def __init__(self, microcontroller: MicroController) -> None:
        super().__init__()
        self.microcontroller = microcontroller

    def execute(self) -> None:
        self.microcontroller._capabilities_read()

class MicrocontrollerConnectionRead(BaseCommand):

    def __init__(self, microcontroller: MicroController) -> None:
        super().__init__()
        self.microcontroller = microcontroller

    def execute(self) -> None:
        self.microcontroller._connection_read()

class SensorIdentify(BaseCommand):

    def __init__(self, sensor: Sensor) -> None:
        super().__init__()
        self.sensor = sensor

    def execute(self) -> None:
        self.sensor._identify()

class ActuatorIdentify(BaseCommand):

    def __init__(self, actuator: Actuator) -> None:
        super().__init__()
        self.actuator = actuator

    def execute(self) -> None:
        self.actuator._identify()


