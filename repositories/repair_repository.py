"""
LaundryBot V7 Enterprise
Repair Repository
"""

from repositories.base_repository import BaseRepository


class RepairRepository(BaseRepository):

    # ==========================================================
    # Read
    # ==========================================================

    def get_all(self):

        return self.fetch_all("""
            SELECT *
            FROM repair_history
            ORDER BY repair_date DESC, id DESC
        """)

    def get(self, repair_id):

        return self.fetch_one("""
            SELECT *
            FROM repair_history
            WHERE id=?
        """, (repair_id,))

    def search(self, keyword):

        keyword = f"%{keyword}%"

        return self.fetch_all("""
            SELECT *
            FROM repair_history
            WHERE

                symptom LIKE ?

                OR cause LIKE ?

                OR solution LIKE ?

                OR technician LIKE ?

            ORDER BY repair_date DESC, id DESC
        """, (

            keyword,

            keyword,

            keyword,

            keyword,

        ))

    def get_by_machine(self, machine_id):

        return self.fetch_all("""
            SELECT *
            FROM repair_history
            WHERE machine_id=?
            ORDER BY repair_date DESC
        """, (machine_id,))

    # ==========================================================
    # Create
    # ==========================================================

    def create(self, data):

        return self.execute("""

            INSERT INTO repair_history(

                machine_id,

                repair_date,

                symptom,

                cause,

                solution,

                technician,

                downtime

            )

            VALUES(?,?,?,?,?,?,?)

        """, (

            data.get("machine_id"),

            data.get("repair_date"),

            data.get("symptom"),

            data.get("cause"),

            data.get("solution"),

            data.get("technician"),

            data.get("downtime"),

        ))

    # ==========================================================
    # Update
    # ==========================================================

    def update(self, repair_id, data):

        self.execute("""

            UPDATE repair_history

            SET

                machine_id=?,

                repair_date=?,

                symptom=?,

                cause=?,

                solution=?,

                technician=?,

                downtime=?

            WHERE id=?

        """, (

            data.get("machine_id"),

            data.get("repair_date"),

            data.get("symptom"),

            data.get("cause"),

            data.get("solution"),

            data.get("technician"),

            data.get("downtime"),

            repair_id,

        ))

    # ==========================================================
    # Delete
    # ==========================================================

    def delete(self, repair_id):

        self.execute("""

            DELETE FROM repair_history

            WHERE id=?

        """, (

            repair_id,

        ))


repair_repository = RepairRepository()