from .BaseCommand import BaseCommand, BaseCommandKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Models.WiFiProfile import WifiProfile

#directly export as dict with enum

class WifiProfileCreate(BaseCommand):

    def __init__(self, wifi_profile: WifiProfile) -> None:
        super().__init__()
        self.wifi_profile = wifi_profile

    def execute(self) -> None:
        self.wifi_profile._create()

class WifiProfileRead(BaseCommand):

    def __init__(self, wifi_profile: WifiProfile) -> None:
        super().__init__()
        self.wifi_profile = wifi_profile

    def execute(self) -> None:
        self.wifi_profile._read()

class WifiProfileSelect(BaseCommand):

    def __init__(self, wifi_profile: WifiProfile) -> None:
        super().__init__()
        self.wifi_profile = wifi_profile

    def execute(self) -> None:
        self.wifi_profile._select()

class WifiProfileDelete(BaseCommand):

    def __init__(self, wifi_profile: WifiProfile) -> None:
        super().__init__()
        self.wifi_profile = wifi_profile

    def execute(self) -> None:
        self.wifi_profile._delete()