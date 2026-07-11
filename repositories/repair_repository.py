"""
Image Laundry AI
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
            ORDER BY created_at DESC, id DESC
        """)

    def get(self, repair_id):

        return self.fetch_one("""
            SELECT *
            FROM repair_history
            WHERE id = ?
        """, (repair_id,))

    def search(self, keyword):

        keyword = f"%{keyword}%"

        return self.fetch_all("""
            SELECT *
            FROM repair_history
            WHERE

                job_no LIKE ?

                OR machine_model LIKE ?

                OR complaint LIKE ?

                OR detail LIKE ?

                OR repair_action LIKE ?

                OR result LIKE ?

                OR sap_no LIKE ?

                OR serial_no LIKE ?

            ORDER BY created_at DESC, id DESC
        """, (

            keyword,

            keyword,

            keyword,

            keyword,

            keyword,

            keyword,

            keyword,

            keyword,

        ))

    def get_by_machine(self, machine_id):

        return self.fetch_all("""
            SELECT *
            FROM repair_history
            WHERE machine_id = ?
            ORDER BY created_at DESC
        """, (machine_id,))

    # ==========================================================
    # Create
    # ==========================================================

    def create(self, data):

        return self.execute("""

            INSERT INTO repair_history
            (

                job_no,

                machine_model,

                complaint,

                detail,

                repair_action,

                result,

                sap_no,

                serial_no,

                report_file,

                customer_id,

                technician_id,

                machine_id

            )

            VALUES
            (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )

        """, (

            data.get("job_no"),

            data.get("machine_model"),

            data.get("complaint"),

            data.get("detail"),

            data.get("repair_action"),

            data.get("result"),

            data.get("sap_no"),

            data.get("serial_no"),

            data.get("report_file"),

            data.get("customer_id"),

            data.get("technician_id"),

            data.get("machine_id"),

        ))
    # ==========================================================
    # Create From AI
    # ==========================================================

    def create_ai(self, data):

        # ตรวจสอบข้อมูลซ้ำ
        duplicate = self.fetch_one("""
            SELECT id
            FROM repair_history
            WHERE

                job_no = ?

                OR
                (
                    serial_no = ?
                    AND serial_no <> ''
                )

            LIMIT 1
        """, (

            data.get("job_no"),

            data.get("serial_no"),

        ))

        if duplicate:

            return duplicate["id"]

        return self.create(data)
    # ==========================================================
    # Update
    # ==========================================================

    def update(self, repair_id, data):

        self.execute("""

            UPDATE repair_history

            SET

                job_no = ?,

                machine_model = ?,

                complaint = ?,

                detail = ?,

                repair_action = ?,

                result = ?,

                sap_no = ?,

                serial_no = ?,

                report_file = ?,

                customer_id = ?,

                technician_id = ?,

                machine_id = ?,

                updated_at = CURRENT_TIMESTAMP

            WHERE id = ?

        """, (

            data.get("job_no"),

            data.get("machine_model"),

            data.get("complaint"),

            data.get("detail"),

            data.get("repair_action"),

            data.get("result"),

            data.get("sap_no"),

            data.get("serial_no"),

            data.get("report_file"),

            data.get("customer_id"),

            data.get("technician_id"),

            data.get("machine_id"),

            repair_id,

        ))

    # ==========================================================
    # Delete
    # ==========================================================

    def delete(self, repair_id):

        self.execute("""

            DELETE FROM repair_history

            WHERE id = ?

        """, (

            repair_id,

        ))


repair_repository = RepairRepository()
    # ==========================================================
    # Statistics
    # ==========================================================

    def total(self):

        row = self.fetch_one("""
            SELECT COUNT(*) AS total
            FROM repair_history
        """)

        return row["total"]