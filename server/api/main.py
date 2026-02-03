# main.py
from fastapi import FastAPI

from server.api.events.startup import lifespan
from server.api.routes.data import router as data_router
from server.api.routes.ping import router as ping_router
from server.api.routes.register import router as register_router

# --- Pass lifespan when creating app ---
app = FastAPI(lifespan=lifespan)


# --- Handshake route ---
@app.get("/")
async def root():
    return {"handshake": "Diggy Net Server"}


# --- Include routes ---
app.include_router(register_router)

app.include_router(ping_router)

app.include_router(data_router)
