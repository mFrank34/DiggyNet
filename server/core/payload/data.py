# data.py
from pydantic import BaseModel, Field
from typing import Dict, Optional


class Data(BaseModel):
    client_id: str
    client_key: str
    client_type: str
    job_id: str
    job_level: int

    # coordinates as simple table
    location: Dict[str, int] = Field(
        default_factory=lambda: {
            "x": 0,
            "y": 0,
            "z": 0,
        }
    )

    # inventory: slot -> item id (0–15)
    inventory: Dict[int, Optional[str]] = Field(
        default_factory=lambda: {i: None for i in range(16)}
    )

    # vision blocks
    vision: Dict[str, Optional[str]] = Field(
        default_factory=lambda: {
            "top": None,
            "middle": None,
            "bottom": None,
        }
    )
