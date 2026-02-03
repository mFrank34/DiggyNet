# client_state.py

import json
import sqlite3

from server.core.lib.dbbase import DBBase as db
from server.core.payload.returns import JobReturn, inventory, coords


class Client_State(db):
    table_name = "client_state"

    @classmethod
    def init_tables(cls, conn: sqlite3.Connection):
        conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {cls.table_name} (
            client_id TEXT PRIMARY KEY,
            coords TEXT NOT NULL,
            job_id TEXT NOT NULL,
            job_level INTEGER NOT NULL DEFAULT 0,
            inventory TEXT NOT NULL,
            fuel REAL NOT NULL,
            FOREIGN KEY (client_id) REFERENCES clients(id),
            FOREIGN KEY (job_id) REFERENCES jobs(id)
        )
        """)
        conn.commit()

    @classmethod
    def update(cls, conn: sqlite3.Connection, client_id: str, coords_data: dict,
               job_id: str, job_level: int, inventory_data: list, fuel: float):
        """
        Insert or update the client state.
        coords_data: dict with keys x, y, z
        inventory_data: list of 16 strings or None
        """
        conn.execute(f"""
            INSERT INTO {cls.table_name} (client_id, coords, job_id, job_level, inventory, fuel)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(client_id) DO UPDATE SET
                coords = excluded.coords,
                job_id = excluded.job_id,
                job_level = excluded.job_level,
                inventory = excluded.inventory,
                fuel = excluded.fuel
        """, (
            client_id,
            json.dumps(coords_data),
            job_id,
            job_level,
            json.dumps(inventory_data),
            fuel
        ))
        conn.commit()

    @classmethod
    def get_coords(cls, conn: sqlite3.Connection, client_id: str):
        row = cls.query_one(
            conn,
            table=cls.table_name,
            select_column="coords",
            where_column="client_id",
            where_value=client_id
        )
        if not row:
            return None
        coord_data = json.loads(row["coords"])
        return coords(
            x=coord_data.get("x", 0),
            y=coord_data.get("y", 0),
            z=coord_data.get("z", 0)
        )

    @classmethod
    def get_jobs(cls, conn: sqlite3.Connection, client_id: str):
        row = cls.query_row(
            conn,
            table=cls.table_name,
            select_columns=["job_id", "job_level"],
            where_column="client_id",
            where_value=client_id
        )
        if not row:
            return None
        return JobReturn(
            job_id=row["job_id"],
            job_stage=row["job_level"]
        )

    @classmethod
    def get_inventory(cls, conn: sqlite3.Connection, client_id: str):
        row = cls.query_one(
            conn,
            table=cls.table_name,
            select_column="inventory",
            where_column="client_id",
            where_value=client_id
        )
        if not row:
            return None
        inv_data = json.loads(row["inventory"])
        return inventory(slots=inv_data)

    @classmethod
    def get_fuel(cls, conn: sqlite3.Connection, client_id: str):
        row = cls.query_one(
            conn,
            table=cls.table_name,
            select_column="fuel",
            where_column="client_id",
            where_value=client_id
        )
        if not row:
            return None
        return row["fuel"]
