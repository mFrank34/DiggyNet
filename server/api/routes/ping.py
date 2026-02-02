# ping.py

import logging

from fastapi import APIRouter, HTTPException

import server.core.share as share
from server.core.database.clients import Client
from server.core.payload.ping import *

router = APIRouter()
logger = logging.getLogger("router.ping")


@router.get("/ping")
async def ping(data: Ping):
    if not Client.validate(share.DB_CONN, data.turtle_id, data.turtle_key, data.client_type):
        raise HTTPException(status_code=403, detail="Invalid Turtle")

    # --- update last seen ---
    Client.touch(share.DB_CONN, data.turtle_id)

    job = str
    # --- ping decision ---
    if data.fuel_level >= 25.0:
        # plan to use cords to work out the distance
        # from current location to home location
        # get it work out how much fuel need to get home and cache it in client
        job = "home"
    elif data.job == "idle":
        job = "request"
    else:
        job = data.job

    # --- create new payload ---
    response = Pong(
        job=job,
    )
    # --- debug response ---
    logger.debug(f"Pong response {response} to turtle {data.turtle_key}")

    # --- payload response ---
    return response
