# init_db.py

from server.core.database import server
from server.core.database.connection import get_conn


def init_db():
    with get_conn() as conn:
        server.init_table(conn)
