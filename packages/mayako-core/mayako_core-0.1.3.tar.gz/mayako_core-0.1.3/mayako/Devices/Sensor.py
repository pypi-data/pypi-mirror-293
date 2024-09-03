from typing import List, TypeVar, Generic
from dataclasses import dataclass

from .Device import Device
from ..Models.BaseDataModel import BaseDataModel
from .SensorObservable import SensorObservable
from ..Config import CCAPABILITIES

T = TypeVar("T", bound=BaseDataModel)

@dataclass
class SensorCapabilities:
    enable: bool
    sample_rate: int
    data_on_state_change: bool

class Sensor(Generic[T], Device, SensorObservable[T]):

    #Capabilities
    _capabilities: SensorCapabilities
    
    _data: List[T]

    def __init__(self, identity: str, description: str = "") -> None:
        Device.__init__(self, identity=identity, description=description)
        SensorObservable.__init__(self)
        self._data = []
        self._capabilities = SensorCapabilities(
            enable=CCAPABILITIES.DEFAULT_INCLUDE_SENSOR,
            sample_rate=CCAPABILITIES.DEFAULT_SAMPLE_RATE,
            data_on_state_change=CCAPABILITIES.DEFAULT_DATA_ON_CHANGE)
        
    def get_data(self) -> list:
        return self._data.popleft()
    
    def set_data(self, data: T) -> None:       
        self._data.append(data)

        if len(self._observers) > 0:
            self.notify_observers(data)

    def get_capabilities(self) -> SensorCapabilities:
        return self._capabilities
    
    def set_capabilities(self, capabilities: SensorCapabilities) -> None:
        self._capabilities = capabilities

