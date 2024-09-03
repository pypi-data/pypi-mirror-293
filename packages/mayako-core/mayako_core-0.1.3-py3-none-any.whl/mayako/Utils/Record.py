from enum import Enum
from abc import ABC, abstractmethod
from typing import Dict, Optional
from ..Utils.Identity import Identity
from ..Config import CERROR_MESSAGES
from ..Devices.MicroController import MicroController

#https://stackoverflow.com/a/51976841
class RecordMode(str, Enum):
    '''
    This class defines the sensor data recording modes categorized into three modes:

    Attributes:
        SINGLEPOINT: Records a single sensor data point. Useful for device or sensor diagnostics.
        BUFFERED: Captures a series of sensor data points in a defined-size buffer before transmission over the network.
        CONTINUOUS: Captures and continuously sends sensor data points over the network.
    '''

    SINGLEPOINT = "SINGLEPOINT"
    BUFFERED = "BUFFERED"
    CONTINUOUS = "CONTINUOUS"

class RecordBase(ABC):

    identity: str
    description: str
    diagnose: bool
    timestamp: bool
    sequence_number: bool
    _microcontrollers: Dict[str, MicroController]
    
    def __init__(self, identity: str) -> None:
        Identity.register(identity)
        self.identity = identity
        self.description = ""
        self.diagnose = False
        self.timestamp = False
        self.sequence_number = False

        self._microcontrollers = {}
    
    def add_description(self, description: str) -> None:
        if type(description) is not str:
            raise TypeError(CERROR_MESSAGES.DESCRIPTION_WRONG_TYPE)
        
        self.description = description

    def enable_diagnose(self) -> None:
        self.diagnose = True

    def enable_timestamp(self) -> None:
        self.timestamp = True

    def enable_sequence_number(self) -> None:
        self.sequence_number = True

    """ def add_microcontroller(self, *microcontrollers: MicroController) -> None:
        for microcontroller in microcontrollers:
            if not isinstance(microcontroller, MicroController):
                raise TypeError(CERROR_MESSAGES.ALL_ARGUMENTS_MICROCONTROLLER)
            
            if microcontroller.identity in self._microcontrollers:
                continue

            self._microcontrollers[microcontroller.identity] = microcontroller  """            

    def get_microcontroller(self, identity: Identity) -> Optional[MicroController]:
        if identity in self._microcontrollers:
            return self._microcontrollers.get(identity)

        return None

    #TODO
    """ 
    @abstractmethod
    def _read(self) -> None:
        print("reading record from MC_01")
    
    @abstractmethod
    def _create(self) -> None:
        print("sending record to MC_01")

    @abstractmethod
    def _start(self) -> None:
        print("starting record")

    @abstractmethod
    def _stop(self) -> None:
        print("stopping record")
 """

