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
            ORDER BY customer_name
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

                customer_name LIKE ?

                OR address LIKE ?

                OR contact LIKE ?

                OR phone LIKE ?

                OR email LIKE ?

            ORDER BY customer_name
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

    def find_by_name(self, customer_name):

        if not customer_name:

            return None

        return self.fetch_one("""
            SELECT *
            FROM customers
            WHERE LOWER(customer_name)=LOWER(?)
            LIMIT 1
        """, (

            customer_name.strip(),

        ))

    def find_like_name(self, customer_name):

        if not customer_name:

            return None

        keyword = f"%{customer_name.strip()}%"

        return self.fetch_one("""
            SELECT *
            FROM customers
            WHERE LOWER(customer_name) LIKE LOWER(?)
            LIMIT 1
        """, (

            keyword,

        ))

    # ==========================================================
    # Find or Create
    # ==========================================================

    def find_or_create(self, customer_name):

        if not customer_name:

            return None

        customer = self.find_by_name(customer_name)

        if customer:

            return customer["id"]

        customer = self.find_like_name(customer_name)

        if customer:

            return customer["id"]

        return self.execute("""
            INSERT INTO customers
            (
                customer_name
            )
            VALUES
            (
                ?
            )
        """, (

            customer_name.strip(),

        ))

    # ==========================================================
    # Create
    # ==========================================================

    def create(self, data):

        return self.execute("""
            INSERT INTO customers
            (

                customer_name,

                address,

                contact,

                phone,

                email,

                note

            )

            VALUES
            (
                ?,?,?,?,?,?
            )
        """, (

            data.get("customer_name"),

            data.get("address"),

            data.get("contact"),

            data.get("phone"),

            data.get("email"),

            data.get("note"),

        ))

    # ==========================================================
    # Update
    # ==========================================================

    def update(self, customer_id, data):

        self.execute("""
            UPDATE customers
            SET

                customer_name=?,

                address=?,

                contact=?,

                phone=?,

                email=?,

                note=?

            WHERE id=?
        """, (

            data.get("customer_name"),

            data.get("address"),

            data.get("contact"),

            data.get("phone"),

            data.get("email"),

            data.get("note"),

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