from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging
import os
import db
import routes


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

server_key = db.get_server_key()
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
        except:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"invalid json")
            return

        client_id = data.get("id")
        client_key = data.get("key")

        # Registration
        if not client_id or not client_key:
            if data.get("server_key") != server_key:
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"invalid server key")
                return

            new_id, new_key = db.register_client()

            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "id": new_id,
                "key": new_key
            }).encode())
            return

        # Validation
        if not db.validate_client(client_id, client_key):
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b"invalid key")
            return

        # Normal heartbeat
        response = routes.handle_heartbeat(data)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def do_GET(self):
        filename = self.path.lstrip("/")  # e.g. "client.lua"
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


def run():
    HTTPServer(("0.0.0.0", 8000), DiggyNetHandler).serve_forever()


if __name__ == "__main__":
    run()
