from local_switch import LocalSwitch
from time import sleep
from temp_sensor import Sensor


fridge = LocalSwitch("nexa_switch", id=2, unit=0, port=5001)
sensor = Sensor(1)

while(True):
    temp = sensor.temp()
    print("Temperature is :"+str(temp)+" C")
    if(temp > 16):
        fridge.turn_on()
    else:
        fridge.turn_off()
    
    sleep(0.5)
    



        


