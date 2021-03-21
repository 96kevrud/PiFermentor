import threading
from time import sleep

class Controller:
    def __init__(self, sensor, fridge, target_temp):
        self.thread = threading.Thread(target=self._start_fridge_control)
        self.fridge = fridge
        self.sensor = sensor
        self.target_temp = target_temp
        self.temp_delta = 0
        self.calc_avg_limit = 100
        self.history = []
        self.thread.start()
            
    def _start_fridge_control(self):
        while(True):
            temp = self.sensor.temp()
            print("Temperature is :"+ "%.2f" % temp+" C")
            self.update_temp_delta(temp)
            wasON = self.fridge.isON
            if(temp > self.target_temp+self.temp_delta):
                self.fridge.turn_on()
            else:
                self.fridge.turn_off()
                #If fridge has been toggled, compressor needs some rest time
                if(wasON):
                    print("Turned off Fridge, Sleeping for 5min")
                    sleep(5*60)
            
    def update_temp_delta(self, temp):
        self.history.append(temp)
        if(len(self.history) >= self.calc_avg_limit):
            avg = sum(self.history)/len(self.history)
            print("Average temp is: " + "%.3f" % avg + " C")
            self.temp_delta = self.target_temp - avg
            self.history = []
            
                
    
