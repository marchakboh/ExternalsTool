import os
import sys
import json
import shutil
from enum import Enum

ETools_Instance = None

class ETools:

    class SupportedTypes(Enum):
        Mega = 0

    root_folder     = None
    config_folder   = None

    Key_JsonFile        = "Database.json"
    Key_JsonArray       = "Assets"
    Key_TempFolder      = "Temp"

    Key_ColumnName      = "Name"
    Key_ColumnLocation  = "Location"
    Key_ColumnType      = "Type"
    Key_ColumnURL       = "URL"

    def __init__(self) -> None:
        pass

    @staticmethod
    def get():
        global ETools_Instance
        if ETools_Instance is None:
            ETools_Instance = ETools()
        return ETools_Instance
    
    def set_root_folder(self, path):
        self.root_folder = path
    
    def set_config_folder(self, path):
        # create config folder if not exist
        os.makedirs(path, exist_ok=True)
        self.config_folder = path
        # create temp folder for downloads
        temp_path = os.path.join(path, ETools.Key_TempFolder)
        if os.path.exists(temp_path):
            shutil.rmtree(temp_path)
        os.makedirs(temp_path, exist_ok=True)
    
    def get_root_folder(self):
        return self.root_folder
    
    def get_config_folder(self):
        return self.config_folder

    @staticmethod
    def save_config(array_data):
        json_data = { ETools.Key_JsonArray: array_data }
        file_path = os.path.join(ETools.get().config_folder, ETools.Key_JsonFile)
        ETools.save_json_to_file(json_data, file_path)
    
    @staticmethod
    def load_config():
        file_path = os.path.join(ETools.get().config_folder, ETools.Key_JsonFile)
        data = ETools.load_json_from_file(file_path)
        if data is not None:
            return data.get(ETools.Key_JsonArray, None)
        return None
    
    @staticmethod
    def save_json_to_file(data, path):
        with open(path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    
    @staticmethod
    def load_json_from_file(path):
        try:
            with open(path, 'r') as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            return None
    
    @staticmethod
    def get_temp_folder():
        temp_path = os.path.join(ETools.get().config_folder, ETools.Key_TempFolder)
        if not os.path.exists(temp_path):
            os.makedirs(temp_path, exist_ok=True)
        return temp_path
    
    @staticmethod
    def get_file_in_temp():
        temp_folder = ETools.get_temp_folder()
        absolute_paths = [os.path.abspath(os.path.join(temp_folder, filename)) for filename in os.listdir(temp_folder) if os.path.isfile(os.path.join(temp_folder, filename))]

        if len(absolute_paths) > 0:
            return absolute_paths[0]
        
        return ""
    
    @staticmethod
    def get_file_in_folder(path):
        absolute_paths = [os.path.abspath(os.path.join(path, filename)) for filename in os.listdir(path) if os.path.isfile(os.path.join(path, filename))]

        if len(absolute_paths) > 0:
            return absolute_paths[0]
        
        return ""
    
    @staticmethod
    def clean_temp_folder():
        temp_folder = ETools.get_temp_folder()
        for filename in os.listdir(temp_folder):
            file_path = os.path.join(temp_folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                pass
    
    @staticmethod
    def construct_download_command(provider_type, url, working_dir):
        if provider_type == ETools.SupportedTypes.Mega.name:
            return [ETools.get_megatool_path(), "dl", "--path", working_dir, url]
        else:
            return []

    @staticmethod
    def construct_unzip_command(file, dest_folder):
        return ["tar", "-xf", file, "-C", dest_folder]
    
    @staticmethod
    def provide_destination_folder(command):
        if len(command) > 0:
            os.makedirs(command[-1], exist_ok=True)

    @staticmethod
    def replace_zip(command):
        old_value = "%zip%"
        new_value = ETools.get_file_in_temp()
        if new_value == "":
            return command
        unzip_command = [new_value if x == old_value else x for x in command]
        return unzip_command
    
    @staticmethod
    def get_execution_path():
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        else:
            return os.path.dirname(os.path.abspath(__file__))
    
    @staticmethod
    def get_megatool_path():
        execution_path = ETools.get_execution_path()
        return execution_path + "\\..\\Tools\\megatools\\megatools.exe"
