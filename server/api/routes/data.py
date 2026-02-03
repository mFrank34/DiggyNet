# data.py

import logging

from fastapi import APIRouter, HTTPException

import server.core.share as share
from server.core.database.clients import Client
from server.core.payload.data import Data

router = APIRouter()
logger = logging.getLogger("router.data")


@router.post("/data")
async def data(data: Data):
    # --- checking the client auth ---
    if not Client.validate(share.DB_CONN, data.client_id, data.client_key, data.client_type):
        raise HTTPException(status_code=403, detail="Invalid Turtle")

    # --- what happens when i client sends data ---
    Client.touch(share.DB_CONN, data.client_id)

    # --- job update ---

    # --- update location of the client

    # --- update inventory ---

    # --- blocks vision ---

    # --- make a response to the client ---
