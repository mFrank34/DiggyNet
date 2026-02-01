# register.py

import uuid
import logging

from fastapi import APIRouter, HTTPException

from server.core.payload.register import *
import server.core.share as share

router = APIRouter()
logger = logging.getLogger("router.register")

# --- generate client key ---
def generate_key():
    return str(uuid.uuid4())


@router.post("/register")
async def register(data: Register):
    # --- registration Logic ---
    if data.server_key != share.SERVER_KEY:
        logger.error("Invalid server ID")
        raise HTTPException(status_code=403, detail="Server private key is not valid")


    client_id = generate_key()
    client_secret = generate_key()

    # --- response to client ---
    response = Response(
        client_id=client_id,
        client_secret=client_secret
    )

    # --- stores response ---
    share.CLIENTS.append(response)

    # --- return new key for client ---
    return response
