# ping.py
from pydantic import BaseModel


class Ping(BaseModel):
    turtle_id: str
    role: str
    job: str
    fuel_level: float