# connection.py

import os
import sqlite3

DB_FILE = os.path.join(os.path.dirname(__file__), "diggynet.db")


def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn
