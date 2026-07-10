"""
Image Laundry AI
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
            ORDER BY brand, model
        """)

    def get(self, machine_id):

        return self.fetch_one("""
            SELECT *
            FROM machines
            WHERE id = ?
        """, (machine_id,))

    def search(self, keyword):

        keyword = f"%{keyword}%"

        return self.fetch_all("""
            SELECT *
            FROM machines
            WHERE

                brand LIKE ?

                OR model LIKE ?

                OR machine_type LIKE ?

            ORDER BY brand, model
        """, (

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

                brand,

                model,

                machine_type,

                manual_file

            )

            VALUES(?,?,?,?)

        """, (

            data.get("brand"),

            data.get("model"),

            data.get("machine_type"),

            data.get("manual_file"),

        ))

    # ==========================================================
    # Update
    # ==========================================================

    def update(self, machine_id, data):

        self.execute("""

            UPDATE machines

            SET

                brand = ?,

                model = ?,

                machine_type = ?,

                manual_file = ?,

                updated_at = CURRENT_TIMESTAMP

            WHERE id = ?

        """, (

            data.get("brand"),

            data.get("model"),

            data.get("machine_type"),

            data.get("manual_file"),

            machine_id,

        ))

    # ==========================================================
    # Delete
    # ==========================================================

    def delete(self, machine_id):

        self.execute("""

            DELETE FROM machines

            WHERE id = ?

        """, (

            machine_id,

        ))


machine_repository = MachineRepository()