import os
import json

Key_JsonFile = "Database.json"
Key_JsonArray = "Assets"

class ETools:

    ConfigFolder = None

    @staticmethod
    def save_json(array_data):
        json_data = { Key_JsonArray: array_data }

        os.makedirs(ETools.ConfigFolder, exist_ok=True)

        file_path = os.path.join(ETools.ConfigFolder, Key_JsonFile)

        with open(file_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
    
    @staticmethod
    def load_json():
        try:
            with open(ETools.ConfigFolder + "/" + Key_JsonFile, 'r') as file:
                data = json.load(file)
                return data.get(Key_JsonArray, None)
            
        except FileNotFoundError:
            return None
