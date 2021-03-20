import requests
from time import sleep
from w1thermsensor import W1ThermSensor

def turn_on_fridge():
    url_on = "http://localhost:5001/send?protocol=nexa_switch&on=1&id=2&unit=0"
    for x in range(5):
        requests.get(url = url_on)
        time.sleep(0.5)
        
def turn_off_fridge():
    url_off = "http://localhost:5001/send?protocol=nexa_switch&off=1&id=2&unit=0"
    for x in range(5):
        requests.get(url = url_off)
        sleep(0.5)

while(True):
    sensor = W1ThermSensor()
    temp = sensor.get_temperature()
    print(temp)
    sleep(1)


        


