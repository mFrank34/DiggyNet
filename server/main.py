from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

from config import HOST, PORT
import routes


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
        # Serve turtle client code
        if self.path == "/client.lua":
            if not os.path.exists("client.lua"):
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"file not found")
                return

            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()

            with open("client.lua", "rb") as f:
                self.wfile.write(f.read())
            return

        self.send_response(404)
        self.end_headers()


def run():
    print(f"DiggyNet running on {HOST}:{PORT}")
    HTTPServer((HOST, PORT), DiggyNetHandler).serve_forever()


if __name__ == "__main__":
    run()
