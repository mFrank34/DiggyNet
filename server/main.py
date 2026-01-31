from http.server import BaseHTTPRequestHandler, HTTPServer

import json
import os
import db
import uuid

import routes

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")
BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "public")

with open(CONFIG_FILE, "r") as f:
    config_data = json.load(f)

HOST = config_data.get("HOST", "127.0.0.1")
PORT = config_data.get("PORT", 8000)

db.init_db()
server_key = db.get_server_key()
print(f"Server key: {server_key}")  # optional, for debugging


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

        client_id = data.get("client_id")
        client_key = data.get("client_key")

        # first-time client registration
        if not client_id:
            client_id, client_key = db.register_client()
            self.send_response(201)  # created
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "message": "registered",
                "client_id": client_id,
                "client_key": client_key
            }).encode())
            return

        # validate existing client
        if not db.validate_client(client_id, client_key):
            self.send_response(401)  # unauthorized
            self.end_headers()
            self.wfile.write(b"invalid client key")
            return

        # valid client → process heartbeat
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


def run():
    print(f"DiggyNet running on {HOST}:{PORT}")
    HTTPServer((HOST, PORT), DiggyNetHandler).serve_forever()


if __name__ == "__main__":
    run()
