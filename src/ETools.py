import os
import json
from enum import Enum

Key_JsonFile = "Database.json"
Key_JsonArray = "Assets"
Key_TempFolder = "Temp"

Key_ColumnName      = "Name"
Key_ColumnLocation  = "Location"
Key_ColumnType      = "Type"
Key_ColumnURL       = "URL"

class SupportedTypes(Enum):
    Mega = 0

class ETools:

    root_folder = None
    config_folder = None

    @staticmethod
    def save_json(array_data):
        json_data = { Key_JsonArray: array_data }

        os.makedirs(ETools.config_folder, exist_ok=True)

        file_path = os.path.join(ETools.config_folder, Key_JsonFile)

        with open(file_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
    
    @staticmethod
    def load_json():
        try:
            with open(ETools.config_folder + "/" + Key_JsonFile, 'r') as file:
                data = json.load(file)
                return data.get(Key_JsonArray, None)
            
        except FileNotFoundError:
            return None
    
    @staticmethod
    def get_temp_folder():
        path = os.path.join(ETools.config_folder, Key_TempFolder)
        os.makedirs(path, exist_ok=True)
        return path
    
    @staticmethod
    def get_file_in_temp():
        temp_folder = ETools.get_temp_folder()
        absolute_paths = [os.path.abspath(os.path.join(temp_folder, filename)) for filename in os.listdir(temp_folder) if os.path.isfile(os.path.join(temp_folder, filename))]

        if len(absolute_paths) > 0:
            return absolute_paths[0]
        
        return ""
    
    @staticmethod
    def clean_temp_folder():
        temp_folder = ETools.get_temp_folder()
        if os.path.exists(temp_folder) and os.path.isdir(temp_folder):
            for filename in os.listdir(temp_folder):
                file_path = os.path.join(temp_folder, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    pass
    
    @staticmethod
    def construct_download_command(provider_type, url):
        if provider_type == SupportedTypes.Mega.name:
            return [f"{os.path.dirname(os.path.abspath(__file__))}\\..\\Tools\\megatools\\megatools.exe", "dl", "--path", ETools.get_temp_folder(), url]
        else:
            return []

    @staticmethod
    def construct_unzip_command(dest_folder):
        return ["tar", "-xf", "%zip%", "-C", os.path.join(ETools.root_folder, dest_folder)]
    
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
