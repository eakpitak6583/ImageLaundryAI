"""
LaundryBot V7 Enterprise
Machine Repository
"""

from repositories.base_repository import BaseRepository


class MachineRepository(BaseRepository):

    # ==========================================================
    # Read
    # ==========================================================

    def get_all(self):

        return self.fetch_all("""
            SELECT *
            FROM machines
            ORDER BY machine_name, model
        """)

    def get(self, machine_id):

        return self.fetch_one("""
            SELECT *
            FROM machines
            WHERE id=?
        """, (machine_id,))

    def search(self, keyword):

        keyword = f"%{keyword}%"

        return self.fetch_all("""
            SELECT *
            FROM machines
            WHERE

                machine_name LIKE ?

                OR model LIKE ?

                OR serial_number LIKE ?

                OR machine_code LIKE ?

            ORDER BY machine_name
        """, (

            keyword,

            keyword,

            keyword,

            keyword,

        ))

    # ==========================================================
    # Create
    # ==========================================================

    def create(self, data):

        return self.execute("""

            INSERT INTO machines(

                machine_code,

                machine_name,

                model,

                serial_number,

                customer_id

            )

            VALUES(?,?,?,?,?)

        """, (

            data.get("machine_code"),

            data.get("machine_name"),

            data.get("model"),

            data.get("serial_number"),

            data.get("customer_id"),

        ))

    # ==========================================================
    # Update
    # ==========================================================

    def update(self, machine_id, data):

        self.execute("""

            UPDATE machines

            SET

                machine_code=?,

                machine_name=?,

                model=?,

                serial_number=?,

                customer_id=?

            WHERE id=?

        """, (

            data.get("machine_code"),

            data.get("machine_name"),

            data.get("model"),

            data.get("serial_number"),

            data.get("customer_id"),

            machine_id,

        ))

    # ==========================================================
    # Delete
    # ==========================================================

    def delete(self, machine_id):

        self.execute("""

            DELETE FROM machines

            WHERE id=?

        """, (

            machine_id,

        ))


machine_repository = MachineRepository()