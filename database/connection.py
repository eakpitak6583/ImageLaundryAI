from contextlib import contextmanager
import sqlite3

from config import Config


@contextmanager
def get_connection():

    conn = sqlite3.connect(
        Config.DATABASE_PATH,
        check_same_thread=False
    )

    conn.row_factory = sqlite3.Row

    try:

        yield conn

        conn.commit()

    except Exception:

        conn.rollback()

        raise

    finally:

        conn.close()