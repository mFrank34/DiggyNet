import os
import json
import secrets

KEYS_FILE = os.path.join(os.path.dirname(__file__), "keys.json")

# Ensure file exists
if not os.path.exists(KEYS_FILE):
    with open(KEYS_FILE, "w") as f:
        json.dump({"server_key": "", "clients": {}}, f, indent = 4)


def load_keys():
    with open(KEYS_FILE, "r") as f:
        return json.load(f)


def save_keys(keys):
    with open(KEYS_FILE, "w") as f:
        json.dump(keys, f, indent = 4)


def generate_server_key():
    keys = load_keys()
    if not keys["server_key"]:
        keys["server_key"] = secrets.token_hex(32)
        save_keys(keys)
    return keys["server_key"]


def register_client(client_id):
    keys = load_keys()
    if client_id not in keys["clients"]:
        keys["clients"][client_id] = secrets.token_hex(32)
        save_keys(keys)
    return keys["clients"][client_id]


def validate_client(client_id, client_key):
    keys = load_keys()
    return keys["clients"].get(client_id) == client_key
