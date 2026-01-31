from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging
import os

from server import db
from server import routes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load config
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

with open(CONFIG_FILE, "r") as f:
    config_data = json.load(f)

HOST = config_data.get("HOST", "0.0.0.0")
PORT = config_data.get("PORT", 8000)

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "public")

server_key = None

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
            logger.info(f"New client registered: {new_id}")

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

        # --- NEW: handle home coordinates from client ---
        if "home_x" in data and "home_y" in data and "home_z" in data:
            db.set_home_location(
                client_id,
                data["home_x"],
                data["home_y"],
                data["home_z"]
            )

        # Valid heartbeat
        response = routes.handle_heartbeat(data)

        # --- NEW: include stored home coords in response ---
        home = db.get_home_location(client_id)
        if home:
            response["home"] = {
                "x": home[0],
                "y": home[1],
                "z": home[2]
            }

        logger.info(f"Heartbeat OK from {client_id}")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def do_GET(self):
        filename = self.path.lstrip("/")
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
    db.init_db()
    server_key = db.get_server_key()

    logger.info("================================")
    logger.info("      DiggyNet Server Booting")
    logger.info("================================")
    logger.info(f"Host: {HOST}")
    logger.info(f"Port: {PORT}")
    logger.info(f"Static file directory: {BASE_DIR}")
    logger.info("Database initialized")
    logger.info("Server key loaded successfully")
    logger.info(f"Server key:")
    logger.info(f"{server_key}")
    logger.info("================================")

    HTTPServer((HOST, PORT), DiggyNetHandler).serve_forever()


if __name__ == "__main__":
    run()
