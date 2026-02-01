# register.py
from pydantic import BaseModel


class Register(BaseModel):
    server_key: str
    turtle_type: str

class Response(BaseModel):
    client_id: str
    client_secret: str