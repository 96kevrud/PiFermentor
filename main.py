from local_switch import LocalSwitch
from time import sleep
from temp_sensor import Sensor
from webserver import WebServer
from controller import Controller
from http.server import HTTPServer
from temp_sensor_simulator import SimulatorSensor
from spreadsheet_logger import SpreadsheetLogger
from logger import Logger

#Parameters
server_host = "0.0.0.0"
server_port = 8765
switch_port = 5001
sensor_delay = 0.5
log_file = "log.txt"
simulation_mode = True # Use simulated temperature readings for development

# Start sensor and fridge switch
fridge = LocalSwitch("nexa_switch", id=2, unit=0, port=switch_port, simulation_mode=simulation_mode)

if simulation_mode:
    print("Using simulation mode")
    sensor = SimulatorSensor(sensor_delay)
else:
    sensor = Sensor(sensor_delay)

#Start fridge controller
controller = Controller(sensor, fridge, 15, simulation_mode)

#Create and start logger
#logger = Logger(sensor, controller, fridge, log_file)

#Log data into spreadsheet
#Requires credfile generated from google cloud
ss_logger = SpreadsheetLogger(sensor, controller, fridge)

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
