from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

from config import HOST, PORT
import routes

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "public")


class DiggyNetHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path != "/heartbeat":
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"invalid json")
            return

        response = routes.handle_heartbeat(data)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def do_GET(self):
        filename = self.path.lstrip("/")  # "client.lua"

        filepath = os.path.join(BASE_DIR, filename)

        if not os.path.exists(filepath):
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"file not found")
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()

        with open(filepath, "rb") as f:
            self.wfile.write(f.read())

        return

def run():
    print(f"DiggyNet running on {HOST}:{PORT}")
    HTTPServer((HOST, PORT), DiggyNetHandler).serve_forever()


if __name__ == "__main__":
    run()
