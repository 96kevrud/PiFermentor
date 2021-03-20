from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import io
import urllib

class ControlServer(BaseHTTPRequestHandler):
    temp = 0
    def do_POST(self):
        print("POST POST POST")
        length = int(self.headers['Content-Length'])
        post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
        print(int(post_data["temp"][0]))
        self.temp = int(post_data["temp"][0])
        self.do_GET()
        
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with io.open("webpage.html","r", encoding="utf-8") as f:
            text = f.read()
            text = text.replace("%TEMP%", str(self.temp))
            
        self.wfile.write(bytes(text, "utf-8"))


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8765
    webServer = HTTPServer((host, port), ControlServer)
    print("Server started http://%s:%s" % (host, port))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")