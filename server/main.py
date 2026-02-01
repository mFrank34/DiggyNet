# main.py (FastAPI version)

import json
import logging
import os
import mimetypes

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from contextlib import asynccontextmanager
from server.coordination.events import router as event_router

from server import db, routes
from tests.dance import create_dance_job

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load config
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

with open(CONFIG_FILE, "r") as f:
    config_data = json.load(f)

HOST = config_data.get("HOST", "0.0.0.0")
PORT = config_data.get("PORT", 8000)
RESET_DB = config_data.get("RESET_DB", False)

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "public")

server_key = None

app = FastAPI()

# Allow local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Heartbeat Endpoint ---
@app.post("/heartbeat")
async def heartbeat(request: Request):
    global server_key

    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="invalid json")

    client_id = data.get("id")
    client_key = data.get("key")

    # Registration flow
    if not client_id or not client_key:
        if data.get("server_key") != server_key:
            raise HTTPException(status_code=403, detail="invalid server key")

        new_id, new_key = db.register_client()
        logger.info(f"New client registered: {new_id}")
        return JSONResponse(
            status_code=201,
            content={"id": new_id, "key": new_key}
        )

    # Validation
    if not db.validate_client(client_id, client_key):
        raise HTTPException(status_code=401, detail="invalid key")

    # Optional: home coordinate update
    if "home_x" in data and "home_y" in data and "home_z" in data:
        db.set_home_location(
            client_id,
            data["home_x"],
            data["home_y"],
            data["home_z"]
        )

    # Heartbeat → coordination layer
    response = routes.handle_heartbeat(data)

    # Add home coords to response
    home = db.get_home_location(client_id)
    if home:
        response["home"] = {"x": home[0], "y": home[1], "z": home[2]}

    logger.info(f"Heartbeat OK from {client_id}")

    return response


# --- Static File Serving ---
@app.get("/{filename:path}")
async def serve_static(filename: str):
    filepath = os.path.join(BASE_DIR, filename)

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="file not found")

    ctype = mimetypes.guess_type(filepath)[0] or "application/octet-stream"
    return FileResponse(filepath, media_type=ctype)


# --- Startup Banner ---
def info():
    logger.info("================================")
    logger.info("      DiggyNet Server Booting")
    logger.info("================================")
    logger.info(f"Host: {HOST}")
    logger.info(f"Port: {PORT}")
    logger.info(f"Static file directory: {BASE_DIR}")
    logger.info("Database initialized")
    logger.info("Server key loaded successfully")
    logger.info(f"Server key:")
    logger.info(f"{server_key}")
    logger.info("================================")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    if RESET_DB:
        db_path = os.path.join(os.path.dirname(__file__), "diggynet.db")
        if os.path.exists(db_path):
            os.remove(db_path)
            logger.info("Database reset enabled — old DB deleted.")

    db.init_db()
    create_dance_job()

    global server_key
    server_key = db.get_server_key()

    info()  # your startup banner

    yield  # <-- server runs here

    # --- Shutdown (optional) ---
    logger.info("Server shutting down…")


app = FastAPI(lifespan=lifespan)

app.include_router(event_router)
