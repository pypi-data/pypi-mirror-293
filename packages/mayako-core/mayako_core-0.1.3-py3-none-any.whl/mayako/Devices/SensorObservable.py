from typing import List, Callable, Generic, TypeVar
from dataclasses import dataclass

from ..Models import BaseDataModel
from ..Utils.Identity import Identity
from ..Utils.Logger import LoggerInstance, LoggerType
from ..Config import CERROR_MESSAGES

T = TypeVar('T')

@dataclass
class _ObserverPair:
    observer: str
    callback: Callable[[T], None]

class SensorObservable(Generic[T]):
    """
    
    Source
        https://stackoverflow.com/a/624939

    """
    _observers: List[_ObserverPair]
    _logger: LoggerType

    def __init__(self) -> None:
        self._observers = []
        self._logger = LoggerInstance.get()

    def subscribe(self, observer: str, callback: Callable[[T], None]) -> None:
        Identity.register(observer)

        if not callable(callback):
            raise TypeError(CERROR_MESSAGES.TYPE_MUST_BE_CALLABLE)

        self._observers.append(_ObserverPair(observer, callback))
        self._logger.debug(f"{observer} added to SensorObservable")

    def unsubscribe(self, observer: str) -> None:
        length_before = len(self._observers)
        self._observers = [pair for pair in self._observers if pair.observer != observer]

        if len(self._observers) < length_before:
            self._logger.debug(f"{observer} was removed from SensorObservable")
        else:
            self._logger.error(f"could not remove {observer} from SensorObservable")

    def notify_observers(self, data: BaseDataModel) -> None:
        for observer in self._observers:
            observer.callback(data)