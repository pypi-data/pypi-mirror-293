from ..Views.MainView import MainView
from .AddDeviceController import AddDeviceController
from .EditDeviceController import EditDeviceController
from .AddWiFiProfileController import AddWiFiProfileController
from .EditWiFiProfileController import EditWiFiProfileController
from .DownloadArduinoController import DownloadArduinoController
from .HomeController import HomeController
from ...MayakoData import MayakoData

class MainController:

    def __init__(self, main_view: MainView, model: MayakoData) -> None:
        self.model = model
        self.main_view = main_view
        self.home_controller = HomeController(self.main_view, self.model)
        self.add_device_controller = AddDeviceController(self.main_view, self.model)
        self.add_wifi_profile_controller = AddWiFiProfileController(self.main_view, self.model)
        self.edit_wifi_profile_controller = EditWiFiProfileController(self.main_view, self.model)
        self.edit_device_controller = EditDeviceController(self.main_view, self.model)
        self.download_arduino_controller = DownloadArduinoController(self.main_view, self.model)

        #set observable method on model class (central point of mayako)
    
    #define callback functions that are on the model classes

    def start(self) -> None:
        self.main_view.switch("home")
        self.main_view.start_mainloop()

