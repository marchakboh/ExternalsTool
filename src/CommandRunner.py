import os
import subprocess
import threading
from ETools import ETools

class CommandRunner:
    
    def __init__(self):
        self.thread = None

    def run_download_command(self, commands, name, log_callback, end_callback):
        
        def target():
            download_command = commands[0]
            log_callback(f"Downloading: {name}")
            process = subprocess.Popen(download_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            for line in process.stdout:
                log_callback(line.rstrip().replace('Â', ''))
            process.stdout.close()
            process.wait()

            log_callback(f"Downloaded in: {ETools.get_file_in_temp()}")

            unzip_command = ETools.replace_zip(commands[1])
            ETools.provide_destination_folder(unzip_command)
            log_callback("Unzipping...")
            process = subprocess.Popen(unzip_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            for line in process.stdout:
                log_callback(line.rstrip())
            process.stdout.close()
            process.wait()
            log_callback(f"Unzipped: {name}")
            ETools.clean_temp_folder()

            end_callback()

        self.thread = threading.Thread(target=target)
        self.thread.start()
