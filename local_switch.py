import requests
from time import sleep

class LocalSwitch(self, protocol, id, unit, port):

def turn_on():
    url_on = "http://localhost:5001/send?protocol=nexa_switch&on=1&id=2&unit=0"
    for x in range(5):
        requests.get(url = url_on)
        sleep(0.5)
        
def turn_off():
    url_off = "http://localhost:5001/send?protocol=nexa_switch&off=1&id=2&unit=0"
    for x in range(5):
        requests.get(url = url_off)
        sleep(0.5)