# main.py

import logging
import requests

# --- LOGGING SECTION ---
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(name)s  %(message)s"
)

# --- CLIENT DATA ---
SERVER_URL = "http://127.0.0.1:8000/"
logger = logging.getLogger("client.handshake")

# --- SERVER HANDSHAKE ----
def handshake():
    try:
        response = requests.get(SERVER_URL, timeout=5)
        response.raise_for_status()
    except Exception as e:
        print("Error: Connecting to server", e)
        return

    data = response.json()

    # getting a response
    if data.get("handshake") == "Diggy Net server":
        logger.info("Connected to Diggy Net server")
    else:
        logger.error("Unknown server response: %s", data)

if __name__ == "__main__":
    handshake()


