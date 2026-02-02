# startup.py

import os
import uuid
import json

from server.core.database.initialize import initialize
from server.core.database.server import Server
from contextlib import asynccontextmanager
from fastapi import FastAPI

import server.core.share as share
from server.core.constants import SERVER_KEY_PATH


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- initialize DB ---
    conn = initialize()
    share.DB_CONN = conn

    # --- ensure server secure is in database --
    secret = Server.ensure_secret(conn)
    share.SERVER_SECRET = secret
    print(f"Server key initialized: {secret}")

    # --- application layer ---
    yield

    # --- shutdown code  ---
    conn.close()
    print("Server is shutting down…")
