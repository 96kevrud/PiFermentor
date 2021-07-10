import threading
from time import sleep
import random

class SimulatorSensor:
    def __init__(self, read_interval):
        self.thread = threading.Thread(target=self._read_temp_thread)
        self.read_interval = read_interval
        self.temperature = 10
        random.seed(496294)
        self.thread.start()

    def temp(self):
        return self.temperature

    def _read_temp_thread(self):
        while(True):
            self.temperature += (random.random()-0.5)*1.3
            sleep(self.read_interval)
