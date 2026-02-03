from CommandControll import CommandControll
from ETools import ETools

Instance = None

class ConsoleWindow:

    controller = None

    def __init__(self) -> None:
        self.controller = CommandControll()
    
    def run(self):
        self.controller.run_process(ETools.load_config(), self.print_callback)
    
    def print_callback(self, log_str):
        print(log_str)

    @staticmethod
    def start():
        Instance = ConsoleWindow()
        Instance.run()