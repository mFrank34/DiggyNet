# ping.py
from pydantic import BaseModel


class Ping(BaseModel):
    turtle_id: str
    turtle_key: str
    job: str
    fuel_level: float

class Pong(BaseModel):
    job: str
    status: str
