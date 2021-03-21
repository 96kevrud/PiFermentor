from w1thermsensor import W1ThermSensor
import threading
from time import sleep

class Sensor:
    def __init__(self, read_interval):
        self.thread = threading.Thread(target=self._read_temp_thread)
        self.read_interval = read_interval
        self.sensor = W1ThermSensor()
        self.temperature = self.sensor.get_temperature()
        self.thread.start()
        
    def temp(self):
        return self.temperature
    
    def _read_temp_thread(self):
        while(True):
            self.temperature = self.sensor.get_temperature()
            sleep(self.read_interval)