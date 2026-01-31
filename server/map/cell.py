# cell.py
from dataclasses import dataclass, field
import time
from server.db import get_block_name


@dataclass
class Cell:
    block_id: int
    y: int = None
    scanned_at: float = field(default_factory=lambda: time.time())

    @property
    def block(self) -> str:
        return get_block_name(self.block_id)
