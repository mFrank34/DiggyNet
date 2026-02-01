# startup.py

import os
import uuid
import json
from contextlib import asynccontextmanager

from fastapi import FastAPI

import server.core.share as share
from server.core.constants import SERVER_KEY_PATH


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- startup code ---
    if os.path.exists(SERVER_KEY_PATH):
        with open(SERVER_KEY_PATH, "r") as f:
            data = json.load(f)
            share.SERVER_KEY = data.get("server_key")
    else:
        share.SERVER_KEY = str(uuid.uuid4())
        with open(SERVER_KEY_PATH, "w") as f:
            json.dump({"server_key": share.SERVER_KEY}, f)

    print("Server key initialized:", share.SERVER_KEY)

    yield  # <-- this marks the application running

    # --- shutdown code  ---
    print("Server is shutting down…")
