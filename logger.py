import io
import threading
import time

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
            f.write("Target\tDelta\tTemp\tFridge\tTime\n")
            f.close()
        except:
            print("File already exists")
        isFridgeOn = True
        while(True):
            if(self.controller.pilight_error_log_flag):
                self.log_pilight_error()
                self.controller.pilight_error_log_flag = False
            if(isFridgeOn != self.fridge.isON):
                isFridgeOn = self.fridge.isON

                row = "%.1f" % target + "\t"
                row += "%.3f" % delta + "\t"
                row += "%.2f" % temp + "\t"
                row += str(on_off) + "\t"
                row += str(dt_now.strftime("%H:%M:%S")) + "\n"
                with io.open(self.log_file_name,"a", encoding="utf-8") as f:
                    f.write(row)

            time.sleep(1)

    def log_pilight_error(self):
        with io.open(self.log_file_name, "a", encoding="utf-8") as f:
            f.write("Pilight error. Restarting pilight\n")
