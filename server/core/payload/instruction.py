# instruction.py
from typing import List

from pydantic import BaseModel


class Instruction(BaseModel):
    job_id: str
    job_level: int  # expected / current level
    commands: List[str]  # ordered commands to execute
