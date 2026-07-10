"""
Image Laundry AI
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
                OR contact LIKE ?
                OR address LIKE ?
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

                customer_name = ?,

                address = ?,

                contact = ?,

                phone = ?,

                email = ?,

                note = ?,

                updated_at = CURRENT_TIMESTAMP

            WHERE id = ?
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
            DELETE FROM customers
            WHERE id = ?
        """, (customer_id,))


customer_repository = CustomerRepository()