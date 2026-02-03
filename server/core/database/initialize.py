# initialize.py

import sqlite3
import server.core.constants as constants


from server.core.database.clients import Client
from server.core.database.client_state import Client_State
from server.core.database.jobs import Jobs
from server.core.database.server import Server


def initialize(path: str = constants.SERVER_KEY_PATH) -> sqlite3.Connection:
    """Initialize the database"""
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row

    # --- initialize all tables ---
    Client.init_tables(conn)
    Server.init_tables(conn)
    Client_State.init_tables(conn)
    Jobs.init_tables(conn)

    # --- return connection ---
    return conn
