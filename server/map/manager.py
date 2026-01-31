# manager.py

from .chunk import Chunk
from shared.constants import CHUNK_SIZE, WALKABLE


class manager:
    def __init__(self):
        self.chunks = {}

    def _coords(self, x, z):
        cx = x // CHUNK_SIZE
        cz = z // CHUNK_SIZE
        lx = x % CHUNK_SIZE
        lz = z % CHUNK_SIZE
        return cx, cz, lx, lz

    def get_chunk(self, cx, cz):
        key = (cx, cz)
        if key not in self.chunks:
            self.chunks[key] = Chunk(cx, cz)
        return self.chunks[key]

    def get_block(self, x, y, z):
        cx, cz, lx, lz = self._coords(x, z)
        chunk = self.get_chunk(cx, cz)
        return chunk.get_block(lx, lz)

    def update_block(self, x, y, z, block_name):
        cx, cz, lx, lz = self._coords(x, z)
        chunk = self.get_chunk(cx, cz)
        chunk.set_block(lx, lz, block_name)

    def save_all(self):
        for chunk in self.chunks.values():
            chunk.save()

    def is_walkable(self, x, y, z):
        cell = self.get_block(x, y, z)
        if cell is None:
            return False
        return cell in WALKABLE
