# server.py

from server.core.lib.dbbase import DBBase as db
import sqlite3
import secrets


class Server(db):
    table_name = 'server'

    @classmethod
    def init_tables(cls, conn: sqlite3.Connection):
        conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {Server.table_name} 
        (
            secret TEXT NOT NULL
        )
        """)

    @classmethod
    def ensure_secret(cls, conn: sqlite3.Connection) -> str:
        secret: str
        # --- get a key from program if already started up before
        cur = conn.execute(
            f"SELECT secret FROM {Server.table_name} LIMIT 1"
        )

        # --- get the row & return key ---
        row = cur.fetchone()
        if row:
            return row["secret"]

        # --- else no key generate and store new key ---
        secret = secrets.token_urlsafe(32)
        conn.execute(
            f"INSERT INTO {Server.table_name} VALUES (?)", (secret,)
        )
        conn.commit()

        return secret
