import sqlite3

from pathlib import Path


class Connection:
    def __init__(self, path: Path):
        self.path = path

    def __enter__(self):
        self.connection = sqlite3.connect(self.path)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
