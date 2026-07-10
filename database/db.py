import sqlite3
from config import Config


def connect():

    print("=" * 60)
    print("DATABASE =", Config.DATABASE_PATH)
    print("=" * 60)

    conn = sqlite3.connect(
        Config.DATABASE_PATH,
        check_same_thread=False,
    )

    conn.row_factory = sqlite3.Row

    return conn