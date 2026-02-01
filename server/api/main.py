# main.py

from fastapi import FastAPI, HTTPException
from routes.register import Register

app = FastAPI()

@app.get("/")
async def root():
    return {"handshake" : "Diggy Net server" }

register_startup_event(app)

app.include_router(Register)

