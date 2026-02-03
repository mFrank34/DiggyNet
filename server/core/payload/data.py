# data.py

from pydantic import BaseModel

from server.core.payload.returns import Coords, Inventory, Vision


class Data(BaseModel):
    client_id: str
    client_key: str
    client_type: str
    job_id: str
    job_level: int
    fuel: float
    # coordinates as simple table
    location: Coords
    # inventory: slot -> item id (0–15)
    slots: Inventory
    # vision blocks
    vision: Vision

class ReturnData(BaseModel):
    response: str