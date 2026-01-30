from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from config import HOST, PORT
import routes

class DiggyNetHandler(BaseHTTPRequestHandler):
    def do_POSE(self):
        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length)

        try:
            data = json.loads(raw_body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"invalid json")
            return

        # very simple routing
        if self.path == "/hello":
            response = routes.handle_hello(data)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"unknown route")
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

def run():
    print(f"🐢 DiggyNet server running on {HOST}:{PORT}")
    HTTPServer((HOST, PORT), DiggyNetHandler).serve_forever()

if __name__ == "__main__":
    run()
