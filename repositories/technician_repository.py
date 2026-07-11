"""
LaundryBot V7 Enterprise
Technician Repository
"""

from repositories.base_repository import BaseRepository


class TechnicianRepository(BaseRepository):

    # ==========================================================
    # Read
    # ==========================================================

    def get_all(self):

        return self.fetch_all("""
            SELECT *
            FROM technicians
            ORDER BY name
        """)

    def get(self, technician_id):

        return self.fetch_one("""
            SELECT *
            FROM technicians
            WHERE id=?
        """, (technician_id,))

    def search(self, keyword):

        keyword = f"%{keyword}%"

        return self.fetch_all("""
            SELECT *
            FROM technicians
            WHERE

                name LIKE ?

                OR phone LIKE ?

                OR email LIKE ?

                OR position LIKE ?

                OR employee_code LIKE ?

                OR department LIKE ?

            ORDER BY name
        """, (

            keyword,

            keyword,

            keyword,

            keyword,

            keyword,

            keyword,

        ))

    # ==========================================================
    # Find
    # ==========================================================

    def find_by_name(self, name):

        if not name:

            return None

        return self.fetch_one("""
            SELECT *
            FROM technicians
            WHERE LOWER(name)=LOWER(?)
            LIMIT 1
        """, (

            name.strip(),

        ))

    def find_by_employee_code(self, employee_code):

        if not employee_code:

            return None

        return self.fetch_one("""
            SELECT *
            FROM technicians
            WHERE employee_code=?
            LIMIT 1
        """, (

            employee_code.strip(),

        ))

    # ==========================================================
    # Find or Create
    # ==========================================================

    def find_or_create(

        self,

        name,

        employee_code="",

        phone="",

        email="",

        position="",

        department="",

    ):

        technician = None

        if employee_code:

            technician = self.find_by_employee_code(
                employee_code
            )

        if technician is None:

            technician = self.find_by_name(
                name
            )

        if technician:

            return technician["id"]

        return self.create({

            "name": name,

            "employee_code": employee_code,

            "phone": phone,

            "email": email,

            "position": position,

            "department": department,

        })

    # ==========================================================
    # Create
    # ==========================================================

    def create(self, data):

        return self.execute("""
            INSERT INTO technicians
            (

                name,

                phone,

                email,

                position,

                note,

                employee_code,

                department

            )

            VALUES
            (
                ?,?,?,?,?,?,?
            )
        """, (

            data.get("name"),

            data.get("phone"),

            data.get("email"),

            data.get("position"),

            data.get("note"),

            data.get("employee_code"),

            data.get("department"),

        ))

    # ==========================================================
    # Update
    # ==========================================================

    def update(

        self,

        technician_id,

        data,

    ):

        self.execute("""
            UPDATE technicians
            SET

                name=?,

                phone=?,

                email=?,

                position=?,

                note=?,

                employee_code=?,

                department=?

            WHERE id=?
        """, (

            data.get("name"),

            data.get("phone"),

            data.get("email"),

            data.get("position"),

            data.get("note"),

            data.get("employee_code"),

            data.get("department"),

            technician_id,

        ))

    # ==========================================================
    # Delete
    # ==========================================================

    def delete(self, technician_id):

        self.execute("""
            DELETE
            FROM technicians
            WHERE id=?
        """, (

            technician_id,

        ))


technician_repository = TechnicianRepository()