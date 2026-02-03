# jobs.py
import json
import sqlite3
from typing import List

from server.core.lib.dbbase import DBBase as db
from server.core.payload.returns import Job_Return


class Jobs(db):
    table_name = "jobs"

    @classmethod
    def init_tables(cls, conn: sqlite3.Connection):
        conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {cls.table_name} (
            job_id TEXT PRIMARY KEY,
            job_stage INTEGER NOT NULL,
            commands TEXT NOT NULL
        )
        """)
        conn.commit()

    def get_jobs(cls, conn: sqlite3.Connection, job_id: str):
        row = cls.query_row(
            table=cls.table_name,
            select_columns=("job_id", "job_stage"),
            where_column="job_id",
            where_value=job_id
        )

        if not row:
            return None

        return Job_Return(
            job_id=row["job_id"],
            job_stage=row["job_level"]
        )

    @classmethod
    def add_jobs(cls, conn: sqlite3.Connection, job_id: str, job_stage: str, commands: List[str]):
        """
        adds jobs to the database
        if the job_id already exists, it will be updated the job stage and commands.
        :param conn: database connection
        :param job_id: id of the job
        :param job_stage: number of stages of a job
        :param commands: list of commands computer
        """
        conn.execute(
            f"""
            INSERT INTO {cls.table_name} (job_id, job_stage, commands)
            VALUES (?, ?, ?)
            ON CONFLICT(job_id) DO UPDATE SET
                job_stage = excluded.job_stage,
                commands = excluded.commands
            """,
            (job_id, job_stage, json.dumps(commands))
        )
        conn.commit()
