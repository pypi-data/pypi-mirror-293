from ..Utils.Identity import Identity
from .Device import Device

class Actuator(Device):

    enabled: bool

    def __init__(self, identity: str, description: str = "") -> None:
       super().__init__(identity=identity, description=description)