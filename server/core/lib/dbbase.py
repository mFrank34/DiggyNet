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
