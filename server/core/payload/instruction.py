# instruction.py
from pydantic import BaseModel
from typing import List


class Instruction(BaseModel):
    job_id: str
    job_level: int  # expected / current level
    commands: List[str]  # ordered commands to execute
