import sqlite3
import os
import secrets
import uuid

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
