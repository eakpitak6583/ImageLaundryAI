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
            ORDER BY brand, model
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

                brand LIKE ?

                OR model LIKE ?

                OR sap_no LIKE ?

                OR serial_no LIKE ?

                OR location LIKE ?

            ORDER BY brand, model
        """, (

            keyword,

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
            WHERE sap_no=?
            LIMIT 1
        """, (

            sap_no.strip(),

        ))

    def find_by_serial(self, serial_no):

        if not serial_no:
            return None

        return self.fetch_one("""
            SELECT *
            FROM machines
            WHERE serial_no=?
            LIMIT 1
        """, (

            serial_no.strip(),

        ))

    def find_by_brand_model(

        self,

        brand,

        model,

    ):

        return self.fetch_one("""
            SELECT *
            FROM machines
            WHERE

                LOWER(brand)=LOWER(?)

                AND

                LOWER(model)=LOWER(?)

            LIMIT 1
        """, (

            brand,

            model,

        ))

    # ==========================================================
    # Find or Create
    # ==========================================================

    def find_or_create(

        self,

        brand,

        model,

        sap_no="",

        serial_no="",

        customer_id=None,

    ):

        machine = None

        if sap_no:

            machine = self.find_by_sap(
                sap_no
            )

        if machine is None and serial_no:

            machine = self.find_by_serial(
                serial_no
            )

        if machine is None:

            machine = self.find_by_brand_model(

                brand,

                model,

            )

        if machine:

            return machine["id"]

        return self.create({

            "brand": brand,

            "model": model,

            "sap_no": sap_no,

            "serial_no": serial_no,

            "customer_id": customer_id,

        })

    # ==========================================================
    # Create
    # ==========================================================

    def create(self, data):

        return self.execute("""
            INSERT INTO machines
            (

                brand,

                model,

                machine_type,

                manual_file,

                sap_no,

                serial_no,

                customer_id,

                machine_master_id,

                location,

                status,

                install_date,

                note

            )

            VALUES
            (
                ?,?,?,?,?,?,?,?,?,?,?,?
            )
        """, (

            data.get("brand"),

            data.get("model"),

            data.get("machine_type"),

            data.get("manual_file"),

            data.get("sap_no"),

            data.get("serial_no"),

            data.get("customer_id"),

            data.get("machine_master_id"),

            data.get("location"),

            data.get("status", "ACTIVE"),

            data.get("install_date"),

            data.get("note"),

        ))

    # ==========================================================
    # Update
    # ==========================================================

    def update(

        self,

        machine_id,

        data,

    ):

        self.execute("""
            UPDATE machines
            SET

                brand=?,

                model=?,

                machine_type=?,

                manual_file=?,

                sap_no=?,

                serial_no=?,

                customer_id=?,

                machine_master_id=?,

                location=?,

                status=?,

                install_date=?,

                note=?

            WHERE id=?
        """, (

            data.get("brand"),

            data.get("model"),

            data.get("machine_type"),

            data.get("manual_file"),

            data.get("sap_no"),

            data.get("serial_no"),

            data.get("customer_id"),

            data.get("machine_master_id"),

            data.get("location"),

            data.get("status"),

            data.get("install_date"),

            data.get("note"),

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