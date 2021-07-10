import threading
import time
from datetime import datetime
import spreadsheet_connector

class SpreadsheetLogger:
    def __init__(self, sensor, controller, fridge):
        self.thread = threading.Thread(target=self._log)
        self.sensor = sensor
        self.controller = controller
        self.fridge = fridge
        self.sleep_time_24h = 2#60*5
        self.sleep_time_all = 10#60*60*24
        self.thread.start()

    def _log(self):
        counter_24h = 0
        counter_all = 0
        while(True):
            temp = self.sensor.temp()
            target = self.controller.target_temp
            delta = self.controller.temp_delta
            dt_now = datetime.now()
            on_off = self.fridge.on_off_str()
            sheet_row_1 = [[dt_now, temp, target, delta, on_off]]
            sheet_row_2 = [[dt_now, temp, target, delta, on_off]]

            if counter_all >= self.sleep_time_all:
                s, ws = spreadsheet_connector.append_row_all(sheet_row_1)
                spreadsheet_connector.append_row_24h(sheet_row_2, s, ws)
                counter_24h = 0
                counter_all = 0
            elif counter_24h >= self.sleep_time_24h:
                spreadsheet_connector.append_row_24h(sheet_row_1)
                counter_24h = 0

            counter_24h += 3
            counter_all += 3
            time.sleep(3)
