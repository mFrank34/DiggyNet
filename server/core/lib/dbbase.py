# dbbase.py
# little base class for creating sqlite3 tables

import json
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
        """
        Query row looks at the row of the table that's selected
        :param conn:  connection to the database
        :param table: table name to look at
        :param select_column: column to look at
        :param where_column: which column to look at
        :param where_value: value to look at
        :return: value of the table
        """
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
        """
        Query row looks at the row of the table that's selected
            :param conn: connection to the database
            :param table: table name to look at
            :param select_columns: columns to look at
            :param where_column: which column to look at
            :param where_value: value to look at
            :return: value of the table
        """
        cols = ", ".join(select_columns)
        cur = conn.execute(
            f"SELECT {cols} FROM {table} WHERE {where_column} = ?",
            (where_value,),
        )

        return cur.fetchone()

    @staticmethod
    def to_json(obj):
        # Pydantic v2
        if hasattr(obj, "model_dump"):
            obj = obj.model_dump()

        # Dataclass
        elif hasattr(obj, "__dataclass_fields__"):
            from dataclasses import asdict
            obj = asdict(obj)

        # Custom class with attributes
        elif hasattr(obj, "__dict__"):
            obj = obj.__dict__

        # Otherwise assume it's already JSON‑safe (dict, list, str, etc.)
        return json.dumps(obj)

    @staticmethod
    def from_json(model_cls, value):
        return model_cls(**json.loads(value))
