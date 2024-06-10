import os
import ETools
from CommandRunner import CommandRunner

class CommandControll:

    def __init__(self):
        self.commands = {}
        self.current_command = ""
        self.log_callback = None
        self.runner = CommandRunner()
    
    def run_process(self, array_data, callback):
        self.commands.clear()
        self.log_callback = callback

        for item in array_data:
            item_name       = item[ETools.Key_ColumnName]
            item_location   = item[ETools.Key_ColumnLocation]
            item_type       = item[ETools.Key_ColumnType]
            item_url        = item[ETools.Key_ColumnURL]

            first_command  = ETools.ETools.construct_download_command(item_type, item_url)
            second_command = ETools.ETools.construct_unzip_command(item_location)

            self.commands[item_name] = [first_command, second_command]

        self.next_command()

    def on_end_process(self):
        self.commands.pop(self.current_command)
        self.next_command()
    
    def next_command(self):
        if len(self.commands.items()) > 0:
            self.current_command = list(self.commands.keys())[0]
            self.runner.run_download_command(self.commands[self.current_command], self.current_command, self.log_callback, self.on_end_process)
        else:
            self.log_callback("Finished")
