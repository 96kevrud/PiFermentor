import threading
from time import sleep
from collections import deque
import os

class Controller:
    def __init__(self, sensor, fridge, target_temp):
        self.thread = threading.Thread(target=self._start_fridge_control)
        self.fridge = fridge
        self.sensor = sensor
        self.target_temp = target_temp
        self.temp_delta = 0
        self.window = deque(maxlen=10000)
        self.thread.start()
        self.pilight_error_log_flag = False
            
    def _start_fridge_control(self):
        while(True):
            temp = self.sensor.temp()
            print("Temperature is :"+ "%.2f" % temp+" C")
            self.update_temp_delta(temp)
            wasON = self.fridge.isON
            if(temp > self.target_temp+self.temp_delta):
                self.fridge.turn_on()
                sleep(30)
            else:
                self.fridge.turn_off()
                #If fridge has been toggled, compressor needs some rest time
                if(wasON):
                    print("Turned off Fridge, Sleeping for 5min")
                    sleep(5*60)

    def check_for_pilight_error(self, temp):
        if(len(self.window)>5000 and temp > self.target_temp+5):
            restart_pilight()
            self.pilight_error_log_flag = True
    def restart_pilight(self):
        os.system("service pilight stop")
        sleep(5)
        os.system("service pilight start")

    def set_target_temp(self, target):
        self.target_temp = target
        self.clear_window()

    def clear_window(self):
        self.window = deque(maxlen=10000)

    def update_temp_delta(self, temp):
        self.window.append(temp)
        avg = sum(self.window)/len(self.window)
        self.temp_delta = self.target_temp - avg

