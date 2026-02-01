# client.py

import sqlite3
import secrets
import uuid

def init_table(conn):
    """Create the table if it doesn't exist."""
    c = conn.cursor()
    conn.execute("""
                 CREATE TABLE IF NOT EXISTS clients
                 (
                     id     TEXT PRIMARY KEY,
                     key    TEXT NOT NULL,
                     home_x INTEGER,
                     home_y INTEGER,
                     home_z INTEGER
                 )
                 """)


def
