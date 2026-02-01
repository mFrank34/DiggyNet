# main.py
from fastapi import FastAPI
from server.api.events.startup import lifespan
from server.api.routes.register import router as register_router  # <-- router object

# --- Pass lifespan when creating app ---
app = FastAPI(lifespan=lifespan)

# --- Handshake route ---
@app.get("/")
async def root():
    return {"handshake": "Diggy Net server"}

# --- Include routes ---
app.include_router(register_router)
