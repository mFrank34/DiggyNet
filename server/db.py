# db.py
import os
import secrets
import uuid
import sqlite3
import time
import zlib

import numpy as np
from shared.constants import CHUNK_SIZE

DB_FILE = os.path.join(os.path.dirname(__file__), "diggynet.db")


def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("""
                  CREATE TABLE IF NOT EXISTS server
                  (
                      id  INTEGER PRIMARY KEY,
                      key TEXT NOT NULL
                  )
                  """)
        c.execute("""
                  CREATE TABLE IF NOT EXISTS clients
                  (
                      id  TEXT PRIMARY KEY,
                      key TEXT NOT NULL
                  )
                  """)
        c.execute("""
                  CREATE TABLE IF NOT EXISTS blocks
                  (
                      id   INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT UNIQUE NOT NULL
                  );
                  """)
        c.execute("""
                  CREATE TABLE IF NOT EXISTS chunks
                  (
                      cx         INTEGER NOT NULL,
                      cz         INTEGER NOT NULL,
                      data       BLOB    NOT NULL,
                      updated_at REAL    NOT NULL,
                      PRIMARY KEY (cx, cz)
                  );
                  """)
        conn.commit()


def get_server_key():
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("SELECT key FROM server WHERE id=1")
        row = c.fetchone()
        if row:
            return row["key"]

        key = secrets.token_hex(32)
        c.execute("INSERT INTO server (id, key) VALUES (1, ?)", (key,))
        conn.commit()
        return key


def register_client():
    client_id = uuid.uuid4().hex
    client_key = secrets.token_hex(32)

    with get_conn() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO clients (id, key) VALUES (?, ?)",
                  (client_id, client_key))
        conn.commit()

    return client_id, client_key


def validate_client(client_id, client_key):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("SELECT key FROM clients WHERE id=?", (client_id,))
        row = c.fetchone()
        return bool(row and row["key"] == client_key)


def get_block_id(name: str) -> int:
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM blocks WHERE name=?", (name,))
        row = c.fetchone()

        if row:
            return row["id"]

        # Insert new block
        c.execute("INSERT INTO blocks (name) VALUES (?)", (name,))
        conn.commit()
        return c.lastrowid


def get_block_name(block_id: int) -> str:
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("SELECT name FROM blocks WHERE id=?", (block_id,))
        row = c.fetchone()
        return row["name"] if row else "minecraft:unknown"


def save_chunk(cx, cz, numpy_array):
    compressed = zlib.compress(numpy_array.tobytes())

    with get_conn() as conn:
        conn.execute("""
                     INSERT INTO chunks (cx, cz, data, updated_at)
                     VALUES (?, ?, ?, ?)
                     ON CONFLICT(cx, cz) DO UPDATE SET data=excluded.data,
                                                       updated_at=excluded.updated_at
                     """, (cx, cz, compressed, time.time()))


def load_chunk(cx, cz):
    with get_conn() as conn:
        cur = conn.execute("SELECT data FROM chunks WHERE cx=? AND cz=?", (cx, cz))
        row = cur.fetchone()

        if not row:
            return None

        raw = zlib.decompress(row["data"])
        arr = np.frombuffer(raw, dtype=np.uint16)
        return arr.reshape((CHUNK_SIZE, CHUNK_SIZE))
