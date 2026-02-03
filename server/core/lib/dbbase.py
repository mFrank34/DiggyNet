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
