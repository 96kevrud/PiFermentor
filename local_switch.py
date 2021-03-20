import requests
from time import sleep

class LocalSwitch:
    
    def __init__(self, protocol, id, unit, port):
        self.url_on = "http://localhost:"+str(port)
        self.url_on += "/send?protocol="+protocol+"&on=1&id="+str(2)+"&unit="+str(unit)
        self.url_off = "http://localhost:"+str(port)
        self.url_off += "/send?protocol="+protocol+"&off=1&id="+str(2)+"&unit="+str(unit)
        
    def turn_on(self):
        for x in range(5):
            requests.get(url = self.url_on)
            sleep(0.5)
        
    def turn_off(self):
        for x in range(5):
            requests.get(url = self.url_off)
            sleep(0.5)