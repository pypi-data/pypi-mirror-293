from .BaseCommand import BaseCommand
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Network.WiFiUDP import Wifi

#directly export as dict with enum

class WifiEnable(BaseCommand):

    def __init__(self, wifi: Wifi) -> None:
        super().__init__()
        self.wifi = wifi

    def execute(self) -> None:
        self.wifi._enable()

class WifiDisable(BaseCommand):

    def __init__(self, wifi: Wifi) -> None:
        super().__init__()
        self.wifi = wifi

    def execute(self) -> None:
        self.wifi._disable()