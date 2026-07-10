"""
LaundryBot V7 Enterprise
Customer Repository
"""

from repositories.base_repository import BaseRepository


class CustomerRepository(BaseRepository):

    # ==========================================================
    # Read
    # ==========================================================

    def get_all(self):

        return self.fetch_all("""
            SELECT *
            FROM customers
            ORDER BY name
        """)

    def get(self, customer_id):

        return self.fetch_one("""
            SELECT *
            FROM customers
            WHERE id = ?
        """, (customer_id,))

    def search(self, keyword):

        keyword = f"%{keyword}%"

        return self.fetch_all("""
            SELECT *
            FROM customers
            WHERE

                name LIKE ?

                OR code LIKE ?

                OR address LIKE ?

                OR contact_person LIKE ?

                OR phone LIKE ?

            ORDER BY name
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

    def find_by_name(self, name):

        return self.fetch_one("""
            SELECT *
            FROM customers
            WHERE LOWER(name)=LOWER(?)
            LIMIT 1
        """, (name.strip(),))

    def find_like_name(self, name):

        keyword = f"%{name.strip()}%"

        return self.fetch_one("""
            SELECT *
            FROM customers
            WHERE LOWER(name) LIKE LOWER(?)
            LIMIT 1
        """, (keyword,))

    # ==========================================================
    # Find or Create
    # ==========================================================

    def find_or_create(self, name):

        if not name:

            return None

        customer = self.find_by_name(name)

        if customer:

            return customer["id"]

        customer = self.find_like_name(name)

        if customer:

            return customer["id"]

        customer_id = self.execute("""

            INSERT INTO customers
            (

                name

            )

            VALUES
            (
                ?
            )

        """, (

            name.strip(),

        ))

        return customer_id

    # ==========================================================
    # Create
    # ==========================================================

    def create(self, data):

        return self.execute("""

            INSERT INTO customers
            (

                code,

                name,

                address,

                contact_person,

                phone,

                email

            )

            VALUES
            (
                ?,?,?,?,?,?
            )

        """, (

            data.get("code"),

            data.get("name"),

            data.get("address"),

            data.get("contact_person"),

            data.get("phone"),

            data.get("email"),

        ))

    # ==========================================================
    # Update
    # ==========================================================

    def update(self, customer_id, data):

        self.execute("""

            UPDATE customers

            SET

                code=?,

                name=?,

                address=?,

                contact_person=?,

                phone=?,

                email=?,

                updated_at=CURRENT_TIMESTAMP

            WHERE id=?

        """, (

            data.get("code"),

            data.get("name"),

            data.get("address"),

            data.get("contact_person"),

            data.get("phone"),

            data.get("email"),

            customer_id,

        ))

    # ==========================================================
    # Delete
    # ==========================================================

    def delete(self, customer_id):

        self.execute("""
            DELETE
            FROM customers
            WHERE id=?
        """, (

            customer_id,

        ))


customer_repository = CustomerRepository()