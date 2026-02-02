# client.py

from server.core.lib.dbbase import DBBase as base
import sqlite3
import secrets
import uuid


class Client(base):
    table_name = 'client'

    @classmethod
    def init_tables(cls, conn: sqlite3.Connection):
        conn.execute("""
                     CREATE TABLE IF NOT EXISTS client
                     (
                         id   TEXT PRIMARY KEY,
                         key  TEXT NOT NULL,
                         type TEXT NOT NULL
                     )
                     """)

        conn.execute("""
                     CREATE INDEX IF NOT EXISTS idx_client_auth
                         ON client (id, key)
                     """)

    @classmethod
    def validate(cls, conn, client_id: str, client_key: str, client_type: str) -> bool:
        cur = conn.execute(
            "SELECT 1 FROM client WHERE id = ? AND key = ? AND type = ? ",
            (client_id, client_key, client_type)
        )
        return cur.fetchone() is not None

    @classmethod
    def register(cls, conn: sqlite3.Connection, client_type: str):
        id = uuid.uuid4().hex
        key = secrets.token_urlsafe(32)

        cur = conn.execute(
            "INSERT INTO client (id, key, type) VALUES (?, ?, ?)",
            (id, key, client_type)
        )
        conn.commit()
        return id, key
