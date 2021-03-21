import io
import threading
import time
from datetime import datetime

class Logger:
    def __init__(self, sensor, controller, fridge, log_file_name):
        self.thread = threading.Thread(target=self._log)
        self.sensor = sensor
        self.controller = controller
        self.fridge = fridge
        self.log_file_name = log_file_name
        self.thread.start()    
    
    def _log(self):
        try:
            f = io.open(self.log_file_name,"x")
            f.close()
            f = io.open(self.log_file_name,"w", encoding="utf-8")
            f.write("Target\tTemp\tFridge\tTime\n")
            f.close()
        except:
            print("File already exists")
            
        while(True):
            row = str(self.controller.target_temp) + "\t"
            row += str(self.sensor.temp()) + "\t"
            row += str(self.fridge.on_off_str()) + "\t"
            row += str(datetime.now().strftime("%H:%M:%S")) + "\n"
            with io.open(self.log_file_name,"a", encoding="utf-8") as f:
                f.write(row)
            time.sleep(1)
            
            