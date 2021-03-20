import threading
from time import sleep

class Controller:
    def __init__(self, sensor, fridge, target_temp):
        self.thread = threading.Thread(target=self._start_fridge_control)
        self.fridge = fridge
        self.sensor = sensor
        self.target_temp = target_temp
        self.thread.start()
            
    def _start_fridge_control(self):
        while(True):
            temp = self.sensor.temp()
            preToggle = self.fridge.isON
            print("Temperature is :"+str(temp)+" C")
            
            if(temp > self.target_temp):
                self.fridge.turn_on()
            else:
                self.fridge.turn_off()
            postToggle = self.fridge.isON
            
            #If fridge has been toggled, compressor needs some time
            if(preToggle != postToggle):
                print("Toggled Fridge, Sleeping for 3min")
                sleep(1)  
    