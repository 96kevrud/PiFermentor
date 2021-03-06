import io
import urllib
from http.server import BaseHTTPRequestHandler
import spreadsheet_connector

class WebServer(BaseHTTPRequestHandler):
    sensor = None
    fridge = None
    controller = None
    temp = 0
    def get_response_body(self):
        print(self.sensor.temp())
        with io.open("webpage.html","r", encoding="utf-8") as f:
            text = f.read()
            text = text.replace("%TAR_TEMP%", "%.2f" % self.controller.target_temp)
            text = text.replace("%CUR_TEMP%", "%.2f" % self.sensor.temp())
            text = text.replace("%ON_OFF_FRIDGE%", self.fridge.on_off_str())
            text = text.replace("%NAME_TEMP%", self.controller.name)
        return bytes(text, "utf-8")

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
        if("temp" in post_data):
            try:
                t = int(post_data["temp"][0])
                self.controller.set_target_temp(t)
            except:
                print("Invalid input")
        elif("clear" in post_data):
            spreadsheet_connector.clear_all()
        elif("name" in post_data):
            try:
                name = str(post_data["name"][0])
                self.controller.name = name
                spreadsheet_connector.change_beer_name(name)
            except:
                print("Invalid input")
        self.do_GET()

    def do_GET(self):
        self.send_response(200)
        if self.path.endswith(".css"):
            self.send_header("Content-type", "text/css")
            self.end_headers()
            f = open("mystyle.css")
            body = bytes(f.read(), "utf-8")
            f.close()
        else:
            self.send_header("Content-type", "text/html")
            self.end_headers()
            body = self.get_response_body()

        self.wfile.write(body)
