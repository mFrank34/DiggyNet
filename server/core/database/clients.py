# client.py

from server.core.lib.dbbase import DBBase as db
import sqlite3
import secrets
import time
import uuid


class Client(db):
    table_name = 'client'

    @classmethod
    def init_tables(cls, conn: sqlite3.Connection):
        conn.execute(f"""
                     CREATE TABLE IF NOT EXISTS {cls.table_name}
                     (
                         id   TEXT PRIMARY KEY,
                         key  TEXT NOT NULL,
                         type TEXT NOT NULL,
                         last_seen REAL
                     )
                     """)

        conn.execute(f"""
                     CREATE INDEX IF NOT EXISTS idx_client_auth
                         ON {cls.table_name} (id, key)
                     """)

    @classmethod
    def validate(cls, conn, client_id: str, client_key: str, client_type: str) -> bool:
        cur = conn.execute(
            f"SELECT 1 FROM {cls.table_name} WHERE id = ? AND key = ? AND type = ? ",
            (client_id, client_key, client_type)
        )
        return cur.fetchone() is not None

    @classmethod
    def register(cls, conn: sqlite3.Connection, client_type: str):
        id = uuid.uuid4().hex
        key = secrets.token_urlsafe(32)

        cur = conn.execute(
            f"INSERT INTO {cls.table_name} (id, key, type) VALUES (?, ?, ?)",
            (id, key, client_type)
        )
        conn.commit()
        return id, key

    @classmethod
    def touch(cls, conn: sqlite3.Connection, client_id: str):
        conn.execute(
            f"UPDATE {cls.table_name} SET last_seen = ? WHERE id = ?", (time.time(), client_id)
        )
        conn.commit()
