# heartbeat.py
from pydantic import BaseModel


class Heartbeat(BaseModel):
    turtle_id: str
    role: str
    job: str
    fuel_level: float