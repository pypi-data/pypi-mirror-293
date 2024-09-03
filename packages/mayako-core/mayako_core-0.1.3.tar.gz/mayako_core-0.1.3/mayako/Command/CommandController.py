from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .BaseCommand import BaseCommand, BaseCommandKey

class CommandController:

    commands: dict[BaseCommandKey, BaseCommand]

    def __init__(self) -> None:
        self.commands = {}

    def set_command(self, command_key: BaseCommandKey, command: BaseCommand) -> None:
        self.commands[command_key] = command

    def run_command(self, command_key: BaseCommandKey, *args, **kwargs) -> None:
        if command_key in self.commands:
            self.commands[command_key].execute(*args, **kwargs)


from ..Devices.MicroController import MicroController
from .Devices import MicrocontrollerBatteryRead, MicrocontrollerCapabilitiesRead, DeviceCommandKey

m = MicroController("test")
mc_bat = MicrocontrollerBatteryRead(m)
mc_cap = MicrocontrollerCapabilitiesRead(m)

c = CommandController()
c.set_command(DeviceCommandKey.MICROCONTROLLER_BATTERY_READ, mc_bat)
c.set_command(DeviceCommandKey.MICROCONTROLLER_CAPABILITIES_READ, mc_cap)

c.run_command(DeviceCommandKey.MICROCONTROLLER_BATTERY_READ)

##SHIT, not working for multiple microcontrollers