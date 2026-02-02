# register.py

import uuid
import logging

from fastapi import APIRouter, HTTPException

from server.core.payload.register import *
from server.core.database.clients import Client
import server.core.share as share

router = APIRouter()
logger = logging.getLogger("router.register")


# --- generate client key ---
def generate_key():
    return str(uuid.uuid4())


@router.post("/register")
async def register(data: Register):
    # --- registration Logic ---
    if data.server_key != share.SERVER_SECRET:
        logger.error("Invalid server ID")
        raise HTTPException(status_code=403, detail="Server private key is not valid")

    # --- generate client credentials and store in DB ---
    client_id, client_secret = Client.register(share.DB_CONN, client_type=data.turtle_type)

    # --- response to client ---
    response = Response(
        client_id=client_id,
        client_secret=client_secret
    )

    # --- stores response ---
    logger.info("Registered new client: %s", client_id)

    # --- return new key for client ---
    return response
