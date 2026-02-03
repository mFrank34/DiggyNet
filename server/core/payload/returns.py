# returns.py
from typing import List, Optional

from pydantic import BaseModel, Field


class Coords(BaseModel):
    x: float
    y: float
    z: float

class Job_Return(BaseModel):
    job_id: str
    job_stage: str

# --- data type for inventory for base class ---
class Inventory(BaseModel):
    # looks like magic and it probly is...
    # creates like a list with 16 slots that have None in them
    slots: List[Optional[str]] = Field(default_factory=lambda: [None]*16)

class Vision(BaseModel):
    top: str
    middle: str
    bottom: str