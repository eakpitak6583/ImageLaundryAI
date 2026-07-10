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
            ORDER BY machine_model
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

                machine_model LIKE ?

                OR sap_no LIKE ?

                OR serial_no LIKE ?

                OR location LIKE ?

            ORDER BY machine_model
        """, (

            keyword,

            keyword,

            keyword,

            keyword,

        ))

    # ==========================================================
    # Find
    # ==========================================================

    def find_by_sap(self, sap_no):

        if not sap_no:
            return None

        return self.fetch_one("""
            SELECT *
            FROM machines
            WHERE sap_no = ?
            LIMIT 1
        """, (sap_no.strip(),))

    def find_by_serial(self, serial_no):

        if not serial_no:
            return None

        return self.fetch_one("""
            SELECT *
            FROM machines
            WHERE serial_no = ?
            LIMIT 1
        """, (serial_no.strip(),))

    def find_by_model(self, model):

        if not model:
            return None

        return self.fetch_one("""
            SELECT *
            FROM machines
            WHERE LOWER(machine_model)=LOWER(?)
            LIMIT 1
        """, (model.strip(),))

    # ==========================================================
    # Find or Create
    # ==========================================================

    def find_or_create(

        self,

        model,

        sap_no="",

        serial_no="",

    ):

        machine = self.find_by_sap(sap_no)

        if machine:

            return machine["id"]

        machine = self.find_by_serial(serial_no)

        if machine:

            return machine["id"]

        machine = self.find_by_model(model)

        if machine:

            return machine["id"]

        machine_id = self.execute("""

            INSERT INTO machines
            (

                machine_model,

                sap_no,

                serial_no

            )

            VALUES
            (
                ?,?,?
            )

        """, (

            model,

            sap_no,

            serial_no,

        ))

        return machine_id

    # ==========================================================
    # Create
    # ==========================================================

    def create(self, data):

        return self.execute("""

            INSERT INTO machines
            (

                machine_model,

                sap_no,

                serial_no,

                customer_id,

                location,

                machine_master_id

            )

            VALUES
            (
                ?,?,?,?,?,?
            )

        """, (

            data.get("machine_model"),

            data.get("sap_no"),

            data.get("serial_no"),

            data.get("customer_id"),

            data.get("location"),

            data.get("machine_master_id"),

        ))

    # ==========================================================
    # Update
    # ==========================================================

    def update(self, machine_id, data):

        self.execute("""

            UPDATE machines

            SET

                machine_model=?,

                sap_no=?,

                serial_no=?,

                customer_id=?,

                location=?,

                machine_master_id=?,

                updated_at=CURRENT_TIMESTAMP

            WHERE id=?

        """, (

            data.get("machine_model"),

            data.get("sap_no"),

            data.get("serial_no"),

            data.get("customer_id"),

            data.get("location"),

            data.get("machine_master_id"),

            machine_id,

        ))

    # ==========================================================
    # Delete
    # ==========================================================

    def delete(self, machine_id):

        self.execute("""
            DELETE
            FROM machines
            WHERE id=?
        """, (

            machine_id,

        ))


machine_repository = MachineRepository()