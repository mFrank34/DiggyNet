# data.py

import logging

from fastapi import APIRouter, HTTPException

import server.core.share as share
from server.core.database.client_state import Client_State
from server.core.database.clients import Client
from server.core.payload.data import Data, ReturnData

router = APIRouter()
logger = logging.getLogger("router.data")


@router.post("/data")
async def data(data: Data):
    """An entry point for the data route to understand and update the database with client information."""

    # --- checking the client auth ---
    if not Client.validate(share.DB_CONN, data.client_id, data.client_key, data.client_type):
        raise HTTPException(status_code=403, detail="Invalid Turtle")

    # --- what happens when i client sends data ---
    Client.touch(share.DB_CONN, data.client_id)

    # --- job update ---
    Client_State.update(
        share.DB_CONN,
        data.client_id,
        data.location,
        data.job_id,
        data.job_level,
        data.slots,
        data.fuel
    )

    # --- blocks vision ---

    # --- make a response to the client ---
    payload = ReturnData(
        response="OK"
    )

    return payload
