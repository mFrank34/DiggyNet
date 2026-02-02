# ping.py
from pydantic import BaseModel


class Ping(BaseModel):
    client_id: str
    client_key: str
    client_type: str
    job: str
    fuel_level: float

class Pong(BaseModel):
    job: str
