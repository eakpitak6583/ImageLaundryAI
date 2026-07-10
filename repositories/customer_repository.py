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
            WHERE id=?
        """, (customer_id,))

    def search(self, keyword):

        keyword = f"%{keyword}%"

        return self.fetch_all("""
            SELECT *
            FROM customers
            WHERE

                name LIKE ?

                OR address LIKE ?

                OR phone LIKE ?

                OR email LIKE ?

            ORDER BY name
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

            INSERT INTO customers(

                name,

                address,

                phone,

                email

            )

            VALUES(?,?,?,?)

        """, (

            data.get("name"),

            data.get("address"),

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

                name=?,

                address=?,

                phone=?,

                email=?

            WHERE id=?

        """, (

            data.get("name"),

            data.get("address"),

            data.get("phone"),

            data.get("email"),

            customer_id,

        ))

    # ==========================================================
    # Delete
    # ==========================================================

    def delete(self, customer_id):

        self.execute("""

            DELETE FROM customers

            WHERE id=?

        """, (

            customer_id,

        ))


customer_repository = CustomerRepository()