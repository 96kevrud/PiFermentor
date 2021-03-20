from w1thermsensor import W1ThermSensor
import threading
from time import sleep

class Sensor:
    def __init__(self, read_interval):
        self.thread = threading.Thread(target=self._read_temp_thread)
        self.temp = 0
        self.read_interval = read_interval
        self.sensor = W1ThermSensor()
        print("bajs")
        
    def temp(self):
        self.thread.start()
        return "hej"
    
    def _read_temp_thread(self):
        while(True):
            self.temp = self.sensor.get_temperature()
            sleep(self.read_interval)