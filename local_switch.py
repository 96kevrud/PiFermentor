import requests
from time import sleep

class LocalSwitch:
    
    def __init__(self, protocol, id, unit, port):
        self.url_on = "http://localhost:"+str(port)
        self.url_on += "/send?protocol="+protocol+"&on=1&id="+str(2)+"&unit="+str(unit)
        self.url_off = "http://localhost:"+str(port)
        self.url_off += "/send?protocol="+protocol+"&off=1&id="+str(2)+"&unit="+str(unit)
        self.isON = -1
        
    def turn_on(self):
        self.isON = True
        for x in range(5):
            requests.get(url = self.url_on)
            sleep(0.1)
        
    def turn_off(self):
        self.isON = False
        for x in range(5):
            requests.get(url = self.url_off)
            sleep(0.1)
    def on_off_str(self):
        return "ON" if self.isON else "OFF"