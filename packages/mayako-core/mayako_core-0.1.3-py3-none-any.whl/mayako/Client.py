import os
import json

from .Network import NetworkManager, NetworkProtocol
from .Utils.Logger import LoggerInstance, Logger
from .Config import CCLIENT

class Client:

    _logger: Logger
    _port: int
    _path: str
    _config: dict

    def __init__(self, port: int = CCLIENT.PORT) -> None:
        LoggerInstance.init_logger()
        self._logger = LoggerInstance.get()

        self._port = port
        self._path = os.getcwd()
        self._load_config()

        
        #from config we can create Microcontrollers that have a networkmanager
        #MC inherits NetworkManager and Commands
        #MC lets Client access everything

        #ok, now that we have microcontrollers in the client, the user can add sensors/acutators to it (in fact he just enables them and changes the capabilities)
        #=> we fill the microcontroller by using config?

        #microcontroller must inform about connection and new values => client observes it

        #only create sensors/actuators in client and auto map to the correct microcontroller because we have the uniques names

        # main.py should look like dippid.py
        
    def _load_config(self) -> None:
        if os.path.exists(CCLIENT.CONFIG_FILE_NAME):
            with open(CCLIENT.CONFIG_FILE_NAME) as file:
                self._config = json.load(file)
        else:
            data = {}
            with open(CCLIENT.CONFIG_FILE_NAME, "w") as file:
                json.dump(data, file, indent=4)
                self._config = data

    def _update_config(self) -> None:
        pass
        #load capabilities into _config and update mayako.json from it




        """
        States:
        1 -> Find Devices & 2 -> Changes Settings & WiFi Settings & change Protocol <=== can be one stage (GUI)
        3 -> record started / record stop awaited / save / visualise
        only GUI for visualisation
        stop on keybind that can be changed
        save on end

        based on config

        if config settings for devices do not fit: what do we do?
        -> we dont want to erase
        -> we want to "transfer" the settings to other devices
        => check if connectionparameters fit
        """