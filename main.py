from local_switch import LocalSwitch
from time import sleep
from temp_sensor import Sensor
from webserver import WebServer
from controller import Controller
from http.server import HTTPServer

#Parameters
server_host = "0.0.0.0"
server_port = 8765
switch_port = 5001
sensor_delay = 0.5

# Start sensor and fridge switch
fridge = LocalSwitch("nexa_switch", id=2, unit=0, port=switch_port)
sensor = Sensor(sensor_delay)

#Start fridge controller
controller = Controller(sensor, fridge, 18)

# Start webserver at 192.168.1.32:8765
#  or if hostfile configed fermentor:8765
WebServer.sensor = sensor
WebServer.fridge = fridge
WebServer.controller = controller
addr = (server_host, server_port)
webServer = HTTPServer(addr, WebServer)
print("Server started http://%s:%s" % addr)

try:
    webServer.serve_forever()
except KeyboardInterrupt:
    pass

webServer.server_close()
print("Server stopped.")
