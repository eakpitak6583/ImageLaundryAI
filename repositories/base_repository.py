from database.connection import get_connection


class BaseRepository:

    def fetch_all(self, sql, params=()):
        with get_connection() as conn:
            return conn.execute(sql, params).fetchall()

    def fetch_one(self, sql, params=()):
        with get_connection() as conn:
            return conn.execute(sql, params).fetchone()

    def execute(self, sql, params=()):
        with get_connection() as conn:
            cursor = conn.execute(sql, params)
            return cursor.lastrowid