"""
LaundryBot V7 Enterprise
Repair Repository
"""

from repositories.base_repository import BaseRepository


class RepairRepository(BaseRepository):

    # ==========================================================
    # Read
    # ==========================================================

    def get_all(

        self,

    ):

        return self.fetch_all(

            """
            SELECT *

            FROM repair_history

            ORDER BY

                created_at DESC,

                id DESC
            """

        )

    def get(

        self,

        repair_id,

    ):

        return self.fetch_one(

            """
            SELECT *

            FROM repair_history

            WHERE id = ?

            LIMIT 1
            """,

            (

                repair_id,

            ),

        )

    def search(

        self,

        keyword,

    ):

        keyword = f"%{keyword}%"

        return self.fetch_all(

            """
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

            ORDER BY

                created_at DESC,

                id DESC
            """,

            (

                keyword,

                keyword,

                keyword,

                keyword,

                keyword,

                keyword,

                keyword,

                keyword,

            ),

        )

    def get_by_machine(

        self,

        machine_id,

    ):

        return self.fetch_all(

            """
            SELECT *

            FROM repair_history

            WHERE machine_id = ?

            ORDER BY

                created_at DESC,

                id DESC
            """,

            (

                machine_id,

            ),

        )

    # ==========================================================
    # Exists
    # ==========================================================

    def exists(

        self,

        job_no="",

        serial_no="",

    ):

        return self.fetch_one(

            """
            SELECT

                id

            FROM repair_history

            WHERE

                job_no = ?

                OR

                (

                    serial_no = ?

                    AND serial_no <> ''

                )

            LIMIT 1
            """,

            (

                job_no,

                serial_no,

            ),

        )

    # ==========================================================
    # Create
    # ==========================================================
        def create(

        self,

        data,

    ):

        return self.execute(

            """
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
            """,

            (

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

            ),

        )

    # ==========================================================
    # Create From AI
    # ==========================================================

    def create_ai(

        self,

        data,

    ):

        duplicate = self.exists(

            job_no=data.get(

                "job_no",

                "",

            ),

            serial_no=data.get(

                "serial_no",

                "",

            ),

        )

        if duplicate:

            return duplicate["id"]

        return self.create(

            data,

        )

    # ==========================================================
    # Update
    # ==========================================================
        def update(

        self,

        repair_id,

        data,

    ):

        self.execute(

            """
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
            """,

            (

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

            ),

        )

    # ==========================================================
    # Delete
    # ==========================================================

    def delete(

        self,

        repair_id,

    ):

        self.execute(

            """
            DELETE

            FROM repair_history

            WHERE id = ?
            """,

            (

                repair_id,

            ),

        )

    # ==========================================================
    # Statistics
    # ==========================================================

    def total(

        self,

    ):

        row = self.fetch_one(

            """
            SELECT

                COUNT(*) AS total

            FROM repair_history
            """

        )

        if row is None:

            return 0

        return row.get(

            "total",

            0,

        )

    # ==========================================================
    # Top Machine
    # ==========================================================
        def update(

        self,

        repair_id,

        data,

    ):

        self.execute(

            """
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
            """,

            (

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

            ),

        )

    # ==========================================================
    # Delete
    # ==========================================================

    def delete(

        self,

        repair_id,

    ):

        self.execute(

            """
            DELETE

            FROM repair_history

            WHERE id = ?
            """,

            (

                repair_id,

            ),

        )

    # ==========================================================
    # Statistics
    # ==========================================================

    def total(

        self,

    ):

        row = self.fetch_one(

            """
            SELECT

                COUNT(*) AS total

            FROM repair_history
            """

        )

        if row is None:

            return 0

        return row.get(

            "total",

            0,

        )

    # ==========================================================
    # Top Machine
    # ==========================================================
        def top_machine(

        self,

        limit=10,

    ):

        return self.fetch_all(

            """
            SELECT

                machine_model,

                COUNT(*) AS total

            FROM repair_history

            WHERE

                machine_model IS NOT NULL

                AND machine_model <> ''

            GROUP BY

                machine_model

            ORDER BY

                total DESC,

                machine_model ASC

            LIMIT ?
            """,

            (

                limit,

            ),

        )

    # ==========================================================
    # Top Customer
    # ==========================================================

    def top_customer(

        self,

        limit=10,

    ):

        return self.fetch_all(

            """
            SELECT

                c.customer_name,

                COUNT(*) AS total

            FROM repair_history r

            LEFT JOIN customers c

                ON r.customer_id = c.id

            GROUP BY

                r.customer_id,

                c.customer_name

            ORDER BY

                total DESC,

                c.customer_name ASC

            LIMIT ?
            """,

            (

                limit,

            ),

        )

    # ==========================================================
    # Top Technician
    # ==========================================================

    def top_technician(

        self,

        limit=10,

    ):

        return self.fetch_all(

            """
            SELECT

                t.fullname,

                COUNT(*) AS total

            FROM repair_history r

            LEFT JOIN technicians t

                ON r.technician_id = t.id

            GROUP BY

                r.technician_id,

                t.fullname

            ORDER BY

                total DESC,

                t.fullname ASC

            LIMIT ?
            """,

            (

                limit,

            ),

        )

    # ==========================================================
    # Top Complaint
    # ==========================================================
        def top_complaint(

        self,

        limit=10,

    ):

        return self.fetch_all(

            """
            SELECT

                complaint,

                COUNT(*) AS total

            FROM repair_history

            WHERE

                complaint IS NOT NULL

                AND complaint <> ''

            GROUP BY

                complaint

            ORDER BY

                total DESC,

                complaint ASC

            LIMIT ?
            """,

            (

                limit,

            ),

        )


# ==========================================================
# Singleton
# ==========================================================

repair_repository = RepairRepository()