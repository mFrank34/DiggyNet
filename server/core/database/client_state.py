# client_state.py

import json
import sqlite3

from server.core.lib.dbbase import DBBase as db
from server.core.payload.returns import Job_Return, Inventory, Coords


class Client_State(db):
    table_name = "client_state"

    @classmethod
    def init_tables(cls, conn: sqlite3.Connection):
        conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {cls.table_name} (
            client_id TEXT PRIMARY KEY,
            coords TEXT NOT NULL,
            job_id TEXT NOT NULL,
            job_status INTEGER NOT NULL DEFAULT 0,
            inventory TEXT NOT NULL,
            fuel REAL NOT NULL,
            FOREIGN KEY (client_id) REFERENCES clients(id),
            FOREIGN KEY (job_id) REFERENCES jobs(id)
        )
        """)
        conn.commit()

    @classmethod
    def update(
            cls,
            conn: sqlite3.Connection,
            client_id: str,
            coords_data: Coords,
            job_id: str,
            job_status: int,
            inventory_data: Inventory,
            fuel: float
    ) -> None:
        """
        Insert or update the client state.
        coords_data: dict with keys x, y, z
        inventory_data: list of 16 strings or None
        """
        conn.execute(f"""
            INSERT INTO {cls.table_name} (client_id, coords, job_id, job_status, inventory, fuel)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(client_id) DO UPDATE SET
                coords = excluded.coords,
                job_id = excluded.job_id,
                job_status = excluded.job_status,
                inventory = excluded.inventory,
                fuel = excluded.fuel
        """, (
            client_id,
            cls.to_json(coords_data),
            job_id,
            job_status,
            cls.to_json(inventory_data),
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
        return cls.from_json(Coords, row["coords"])

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
        return Job_Return(
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
        inv_data = cls.from_json(Inventory, row["inventory"])
        return inv_data

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
