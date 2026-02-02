# share.py
import sqlite3

# --- File Locations ---
DATABASE_LOCATION = "server_data.db"

# --- DATABASE ---
DB_CONN: sqlite3.Connection | None = None

# --- Server Secrit ---
SERVER_SECRET: str | None = None
