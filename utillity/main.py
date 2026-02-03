import logging
import httpx

from server.core.payload.ping import *
from server.core.payload.register import *

# --- LOGGING SECTION ---
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(name)s  %(message)s"
)
logger = logging.getLogger("client.handshake")

# --- CLIENT CONFIG ---
SERVER_URL = "http://127.0.0.1:8000"
SERVER_KEY = "4YoAEameV4W7ZuOOGihH_wBkm4rXufeRlxhhKZso4ls"

# --- Client creds ---
CLIENT_TYPE = "turtle"

# --- SERVER HANDSHAKE ---
def handshake() -> bool:
    try:
        response = httpx.get(SERVER_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        logger.error("Error connecting to server: %s", e)
        return False

    if data.get("handshake") == "Diggy Net Server":
        logger.info("Diggy Net server is alive")
        return True
    else:
        logger.error("Unknown server response: %s", data)
        return False


# --- REGISTER CLIENT ---
def register(server_url: str, server_key: str, turtle_type: str) -> Response:
    global CLIENT_ID, CLIENT_SECRET
    payload = Register(
        server_key=server_key,
        turtle_type=turtle_type
    )

    with httpx.Client(timeout=5) as client:
        response = client.post(f"{server_url}/register", json=payload.model_dump())
        response.raise_for_status()
        data = response.json()

        CLIENT_ID = data["client_id"]
        CLIENT_SECRET = data["client_secret"]

        return Response(**data)


# --- PING SERVER ---
def ping(server_url: str, client_id: str, client_key: str, client_type: str, fuel: float) -> Pong:
    payload = Ping(
        client_id=client_id,
        client_key=client_key,
        client_type=client_type,
        job="idle",
        fuel_level=fuel
    )

    with httpx.Client(timeout=5) as client:
        response = client.post(f"{server_url}/ping", json=payload.model_dump())
        response.raise_for_status()
        data = response.json()
        return Pong(**data)


if __name__ == "__main__":
    handshake = handshake()
    if handshake:
        client_response = register(SERVER_URL, SERVER_KEY, CLIENT_TYPE)
        logger.info(
            "Registration successful: Client ID = %s, Secret = %s",
            client_response.client_id,
            client_response.client_secret
        )

    if handshake:
        client_response = ping(SERVER_URL, CLIENT_ID, CLIENT_SECRET, CLIENT_TYPE, 0.30)
        logger.info(
            "Ping successful: Given Job = %s",
            client_response.job
        )
