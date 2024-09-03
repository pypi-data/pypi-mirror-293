from .Controllers.MainController import MainController
from .Views.MainView import MainView
from ..Utils.Logger import LoggerInstance, LoggingLevel
from ..MayakoData import MayakoData

#https://nazmul-ahsan.medium.com/how-to-organize-multi-frame-tkinter-application-with-mvc-pattern-79247efbb02b
#https://realpython.com/python-gui-tkinter/


def run() -> None:
    LoggerInstance.init_logger(logging_level=LoggingLevel.DEBUG)
    model = MayakoData()
    main_view = MainView()
    main_controller = MainController(main_view, model)
    main_controller.start()

if __name__ == "__main__":
    run()