from pathlib import Path
from .connection import Connection
from .database import Database


db = Database(Path('instance/data.db'))
