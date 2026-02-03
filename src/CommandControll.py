import os
import shutil
from ETools import ETools
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
        
        if array_data is None:
            return

        for item in array_data:
            item_name       = item[ETools.Key_ColumnName]
            item_location   = item[ETools.Key_ColumnLocation]
            item_type       = item[ETools.Key_ColumnType]
            item_url        = item[ETools.Key_ColumnURL]

            self.commands[item_name] = [False, item_location, item_type, item_url]

        self.next_command()

    def on_end_process(self):
        if self.commands[self.current_command][0] is True:
            working_dir = os.path.join(ETools.get().get_temp_folder(), self.current_command)
            if os.path.exists(working_dir):
                shutil.rmtree(working_dir)
            self.commands.pop(self.current_command)
        else:
            self.commands[self.current_command][0] = True

        self.next_command()
    
    def next_command(self):
        if len(self.commands.items()) > 0:
            self.current_command = list(self.commands.keys())[0]
            
            command_data = self.commands[self.current_command]
            command = []
            working_dir = os.path.join(ETools.get().get_temp_folder(), self.current_command)
            if command_data[0] is False: # need to download
                self.log_callback(f"\nUploading file: {self.current_command}")
                os.makedirs(working_dir, exist_ok=True)
                command = ETools.construct_download_command(command_data[2], command_data[3], working_dir)
            else: # need to unzip if can
                file_path = ETools.get_file_in_folder(working_dir)
                dest_folder = os.path.join(ETools.get().get_root_folder(), command_data[1])
                os.makedirs(dest_folder, exist_ok=True)
                if file_path.endswith(".rar"):
                    self.log_callback(f"\nUnzipping file: {self.current_command}")
                    command = ETools.construct_unzip_command(file_path, dest_folder)
                else:
                    self.log_callback(f"\nMoving file: {self.current_command}")
                    shutil.move(file_path, dest_folder)
                
            self.runner.run_command(command, self.log_callback, self.on_end_process)
        else:
            self.log_callback("Finished")
