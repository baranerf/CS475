from os import getenv
from pathlib import Path

ROOT_DIR = Path(".").absolute()

DATABASE = getenv("DATABASE", "test.sqlite3")
