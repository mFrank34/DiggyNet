# server.py

import sqlite3
import secrets


def init_table(conn):
    """Create the server table if it doesn’t exist."""
    c = conn.cursor()
    c.execute("""
              CREATE TABLE IF NOT EXISTS server
              (
                  id  INTEGER PRIMARY KEY,
                  key TEXT NOT NULL
              )
              """)


def get_server_key(conn):
    """Fetch the server key, or generate one if it doesn't exist."""
    c = conn.cursor()
    c.execute("SELECT key FROM server WHERE id=1")
    row = c.fetchone()
    if row:
        return row["key"]

    # generate new key
    key = secrets.token_hex(32)
    c.execute("INSERT INTO server (id, key) VALUES (1, ?)", (key,))
    conn.commit()
    return key


def set_server_key(conn, key):
    """Overwrite server key if needed."""
    c = conn.cursor()
    c.execute("UPDATE server SET key=? WHERE id=1", (key,))
    conn.commit()
