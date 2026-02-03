# returns.py
from typing import List, Optional

from pydantic import BaseModel, Field


class coords(BaseModel):
    x: float
    y: float
    z: float

class JobReturn(BaseModel):
    job_id: str
    job_stage: str

# --- data type for inventory for base class ---
class inventory(BaseModel):
    # looks like magic and it probly is...
    # creates like a list with 16 slots that have None in them
    slots: List[Optional[str]] = Field(default_factory=lambda: [None]*16)
