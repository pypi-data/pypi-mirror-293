import json
from typing import List
import os

from regex import F

from .Observable import Observable
from .Models.WiFiProfile import WiFiProfile
from .Service.SerialScanner import SerialInfo
from .Service.BLEScanner import BLEInfo
from .Models.User import User
from .Devices.MicroController import MicroControllerCapabilities
from .Network.NetworkInterface import NetworkProtocols
from .Config import CCLIENT
from .Utils.Logger import LoggerType, LoggerInstance
from .Service.MacAdress import get_macaddress

class MayakoData(Observable):

    """
    Source
        https://stackoverflow.com/a/51976841
    """

    this_user: User
    all_users: List[User]
    wifi_profiles: List[WiFiProfile]
    serial_ports: List[SerialInfo]
    ble_addresses: List[BLEInfo]
    microcontrollers: List[MicroControllerCapabilities]
    logger: LoggerType
    selected_wifi_profile: WiFiProfile
    selected_microcontroller: MicroControllerCapabilities

    def __init__(self) -> None:
        super().__init__()
        self.logger = LoggerInstance.get()
        self.this_user = None
        self.all_users = []
        self.wifi_profiles = []
        self.serial_ports = []
        self.ble_addresses = []
        self.microcontrollers = []
        self.selected_wifi_profile = None
        self.selected_microcontroller = None
        
        self._check_if_file_exists()
        self._load_from_file()
        self._save_to_file()

        self._self_bind()

    def _check_if_file_exists(self) -> None:
        curr_workdir = os.getcwd()
        config_file_path = os.path.join(curr_workdir, CCLIENT.CONFIG_FILE_NAME)
        
        if not os.path.exists(config_file_path):
            with open(config_file_path, "w") as file:
                file.write("{}")
        else:
            self.logger.debug(f"{CCLIENT.CONFIG_FILE_NAME} already exists")

    def _load_from_file(self) -> None:
        with open(CCLIENT.CONFIG_FILE_NAME, "r") as file:
            data = json.load(file)
            
            if "wifi_profiles" in data:
                # Load wifi profiles
                wifi_profiles = [WiFiProfile.from_dict(wifi_profile) for wifi_profile in data["wifi_profiles"]]
                self.add_wifi_profile(wifi_profiles)
            
            if "ble_addresses" in data:
                # Load BLE addresses
                ble_addresses = [BLEInfo.from_dict(item) for item in data["ble_addresses"]]
                self.add_ble_address(ble_addresses)
            
            if "microcontrollers" in data:
                # Load microcontrollers
                microcontrollers = [MicroControllerCapabilities.from_dict(item) for item in data["microcontrollers"]]
                self.add_microcontroller(microcontrollers)
            
            if "users" in data:
                # Load users
                self.all_users = [User.from_dict(u) for u in data["users"]]
                self.this_user = self._check_user(self.all_users)

    def _save_to_file(self, *_) -> None:
        d = {
            "users": [],
            "wifi_profiles": [],
            "ble_addresses": [],
            "microcontrollers": []
        }

        for user in self.all_users:
            d["users"].append(user.to_dict())
        
        for wifi_profile in self.wifi_profiles:
            d["wifi_profiles"].append(wifi_profile.to_dict())

        for ble_address in self.ble_addresses:
            d["ble_addresses"].append(ble_address.to_dict())

        for microcontroller in self.microcontrollers:
            d["microcontrollers"].append(microcontroller.to_dict())

        with open(CCLIENT.CONFIG_FILE_NAME, "w") as file:
            json.dump(d, file, indent=4)

    def _self_bind(self) -> None:
        self.subscribe("wifi_profiles_update", self._save_to_file)
        self.subscribe("microcontrollers_update", self._save_to_file)
        self.subscribe("serial_ports_update", self._save_to_file)
        self.subscribe("user_update", self._save_to_file)
        self.subscribe("ble_addresses_update", self._save_to_file)

    def _check_user(self, users: List[User]) -> User:
        user_address = get_macaddress()
        user = None
    
        for u in users:
            if u.user_mac_address == user_address:
                user = u
                return user
        
        new_user = User(user_mac_address=user_address, arduino_folder=CCLIENT.DEFAULT_ARDUINO_FOLDER)

        if new_user not in self.all_users:
            self.all_users.append(new_user)
            
        return new_user

    def add_wifi_profile(self, wifi_profiles: List[WiFiProfile]) -> None:
        for wifi_profile in wifi_profiles:
            if wifi_profile in self.wifi_profiles:
                continue
            
            self.wifi_profiles.append(wifi_profile)

        self.notify_observers("wifi_profiles_update")

    def remove_wifi_profile(self, wifi_profile: WiFiProfile) -> None:
        self.wifi_profiles.remove(wifi_profile)

        self.notify_observers("wifi_profiles_update")

    def get_wifi_profiles(self) -> List[WiFiProfile]:
        return self.wifi_profiles
    
    def select_wifi_profile(self, wifi_profile: WiFiProfile) -> None:
        if wifi_profile not in self.wifi_profiles:
            self.select_wifi_profile = self.wifi_profiles[0]
            self.logger.error("unknown wifi_profile selected")
        
        self.selected_wifi_profile = wifi_profile
        self.notify_observers("wifi_profile_selected")

    def update_wifi_profile(self, updated_wifi_profile: WiFiProfile) -> None:
        for index, wifi_profile in enumerate(self.wifi_profiles):
            if updated_wifi_profile.wifi_key == wifi_profile.wifi_key:                
                self.wifi_profiles[index] = updated_wifi_profile
                break

        self.notify_observers("wifi_profiles_update")

    def add_microcontroller(self, microcontrollers: List[MicroControllerCapabilities]) -> None:
        for microcontroller in microcontrollers:
            if microcontroller in self.microcontrollers:
                continue
        
            self.microcontrollers.append(microcontroller)

        self.notify_observers("microcontrollers_update")
    
    def remove_microcontroller(self, microcontroller: MicroControllerCapabilities) -> None:
        self.microcontrollers.remove(microcontroller)

        self.notify_observers("microcontrollers_update")

    def get_microcontrollers(self) -> List[MicroControllerCapabilities]:
        return self.microcontrollers
    
    def select_microcontroller(self, microcontroller: MicroControllerCapabilities) -> None:
        if microcontroller not in self.microcontrollers:
            self.select_microcontroller = self.microcontrollers[0]
            self.logger.error("unknown microcontroller selected")
        
        self.selected_microcontroller = microcontroller
        self.notify_observers("microcontroller_selected")

    def add_serial_port(self, serial_ports: List[SerialInfo]) -> None:
        for serial_port in serial_ports:
            if serial_port in self.serial_ports:
                continue
        
            self.serial_ports.append(serial_port)
        
        self.notify_observers("serial_ports_update")

    def remove_serial_port(self, serial_port: SerialInfo) -> None:
        self.serial_ports.remove(serial_port)

        self.notify_observers("serial_ports_update")

    def get_serial_ports(self) -> List[SerialInfo]:
        return self.serial_ports
    
    def add_user(self, user: User) -> None:
        self.this_user.arduino_folder = user.arduino_folder

        self.notify_observers("user_update")

    def get_users(self) -> List[User]:
        return self.users
    
    def get_this_user(self) -> User:
        return self.this_user
    
    def add_ble_address(self, ble_addresses: List[BLEInfo]) -> None:
        for ble_address in ble_addresses:
            if ble_address in self.ble_addresses:
                continue

            self.ble_addresses.append(ble_address)

        self.notify_observers("ble_addresses_update")
    
    def remove_ble_address(self, ble_address: BLEInfo) -> None:
        self.ble_addresses.remove(ble_address)

        self.notify_observers("ble_addresses_update")

    def get_ble_addresses(self) -> List[BLEInfo]:
        return self.ble_addresses

    """
    if an object changes, we also need methods...
    we need to bind on all notifies here and safe all data back to config
    
    """

