import tkinter as tk
import json
from ..Views.MainView import MainView
from ..Views.EditDeviceView import EditDeviceView
from ...MayakoData import MayakoData

class EditDeviceController:

    main_view: MainView
    edit_device_frame: EditDeviceView

    def __init__(self, main_view: MainView, model: MayakoData) -> None:
        self.model = model
        self.main_view = main_view
        self.edit_device_frame = self.main_view.frame_classes["edit_device"]
        self._bind()
        self._model_subscribe()

    def _bind(self) -> None:
        self.edit_device_frame.return_btn.config(command=self._return_to_main)
        self.edit_device_frame.update_capabilities_btn.config(command=self._update_capabilities)

    def _return_to_main(self) -> None:
        self.main_view.switch("home")

    def _model_subscribe(self) -> None:
        self.model.subscribe("microcontroller_selected", self._load_microcontroller)

    def _load_microcontroller(self, mayako_data: MayakoData) -> None:
        mc = mayako_data.selected_microcontroller
        self.edit_device_frame.identity_text.config(text=mc.identity)
        self.edit_device_frame.protocol_text.config(text=f"{mc.protocol} -- {"online" if mc.online else "offline"}")
        self.edit_device_frame.battery_text.config(text=f"{mc.battery["percentage"]}% -- {'charging' if mc.battery["charging"] else 'running on battery'}")

        self.edit_device_frame.capabilities_text.delete("1.0", tk.END)
        self.edit_device_frame.capabilities_text.insert(tk.END, json.dumps(mc.to_dict(), indent=4))
        
    def _update_capabilities(self) -> None:
        #TODO: retrieve capabilities from the specific microcontroller
        # update the information in MayakoData
        print("NYI")
        pass