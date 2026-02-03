import os
import subprocess
import threading
from ETools import ETools

class CommandRunner:
    
    def __init__(self):
        self.thread = None

    def run_command(self, command, log_callback, end_callback):
        
        if len(command) <= 0:
            end_callback()
        else:
            def target():
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                for line in process.stdout:
                    log_callback(line.rstrip().replace('Â', ''))
                process.stdout.close()
                process.wait()
                end_callback()

            self.thread = threading.Thread(target=target)
            self.thread.start()
