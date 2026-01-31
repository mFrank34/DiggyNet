# chunk.py
import numpy as np
from server.db import get_block_id, get_block_name, save_chunk, load_chunk
from server.shared.constants import CHUNK_SIZE


class Chunk:
    def __init__(self, cx, cz):
        self.cx = cx
        self.cz = cz
        self.data = np.zeros((CHUNK_SIZE, CHUNK_SIZE), dtype=np.uint16)
        self.dirty = False

        # Try loading from DB
        loaded = load_chunk(cx, cz)
        if loaded is not None:
            self.data = loaded

    def set_block(self, lx, lz, block_name):
        block_id = get_block_id(block_name)
        self.data[lx, lz] = block_id
        self.dirty = True

    def get_block(self, lx, lz):
        block_id = int(self.data[lx, lz])
        return get_block_name(block_id)

    def save(self):
        if self.dirty:
            save_chunk(self.cx, self.cz, self.data)
            self.dirty = False
