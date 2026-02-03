# dbbase.py
# little base class for creating sqlite3 tables

import sqlite3
from abc import ABC, abstractmethod


class DBBase(ABC):
    table_name: str

    @classmethod
    @abstractmethod
    def init_tables(cls, conn: sqlite3.Connection):
        """Create table schema"""
        pass

    @staticmethod
    def query_one(
            conn: sqlite3.Connection,
            table: str,
            select_column: str,
            where_column: str,
            where_value
    ):
        cur = conn.execute(
            f"SELECT {select_column} FROM {table} WHERE {where_column} = ?",
            (where_value,)
        )
        row = cur.fetchone()
        return row[select_column] if row else None

    @staticmethod
    def query_row(
            conn: sqlite3.Connection,
            table: str,
            select_columns: list[str],
            where_column: str,
            where_value,
    ):
        cols = ", ".join(select_columns)
        cur = conn.execute(
            f"SELECT {cols} FROM {table} WHERE {where_column} = ?",
            (where_value,),
        )
        return cur.fetchone()
