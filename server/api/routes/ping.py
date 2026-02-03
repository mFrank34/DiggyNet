# ping.py

import logging

from fastapi import APIRouter, HTTPException

import server.core.share as share
from server.core.database.clients import Client
from server.core.payload.ping import *

router = APIRouter()
logger = logging.getLogger("router.ping")


@router.post("/ping")
async def ping(data: Ping):
    if not Client.validate(share.DB_CONN, data.client_id, data.client_key, data.client_type):
        raise HTTPException(status_code=403, detail="Invalid Turtle")

    # --- update last seen ---
    Client.touch(share.DB_CONN, data.client_id)

    job = str
    # --- ping decision ---
    if data.fuel_level <= 0.25:
        # plan to use cords to work out the distance
        # from current location to home location
        # get it work out how much fuel need to get home and cache it in client
        job = "home"
    elif data.job == "idle":
        # if turtle is idle, force it to make a new request to instructions or data
        job = "request"
    else:
        job = data.job

    # --- create new payload ---
    response = Pong(
        job=job
    )
    # --- debug response ---
    logger.debug(f"Pong response {response} to turtle {data.client_key}")

    # --- payload response ---
    return response
