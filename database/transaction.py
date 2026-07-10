from database.connection import get_connection


class Transaction:

    def __enter__(self):

        self.ctx = get_connection()

        self.conn = self.ctx.__enter__()

        return self.conn

    def __exit__(

        self,

        exc_type,

        exc,

        tb

    ):

        return self.ctx.__exit__(

            exc_type,

            exc,

            tb

        )