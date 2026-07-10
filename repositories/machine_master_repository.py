"""
LaundryBot V7 Enterprise
Machine Master Repository
"""

from repositories.base_repository import BaseRepository


class MachineMasterRepository(BaseRepository):

    # ==========================================================
    # Read
    # ==========================================================

    def get_all(self):

        return self.fetch_all("""
            SELECT *
            FROM machine_master
            ORDER BY brand, model
        """)

    def get(self, machine_id):

        return self.fetch_one("""
            SELECT *
            FROM machine_master
            WHERE id = ?
        """, (machine_id,))

    def search(self, keyword):

        keyword = f"%{keyword}%"

        return self.fetch_all("""
            SELECT *
            FROM machine_master
            WHERE

                brand LIKE ?

                OR model LIKE ?

                OR machine_type LIKE ?

                OR category LIKE ?

                OR manufacturer LIKE ?

                OR description LIKE ?

            ORDER BY brand, model
        """, (

            keyword,

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

        sql = """
        INSERT INTO machine_master
        (

            brand,

            model,

            machine_type,

            category,

            capacity,

            fuel_type,

            voltage,

            phase,

            frequency,

            manufacturer,

            country,

            manual_file,

            image_file,

            description

        )
        VALUES
        (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """

        return self.execute(sql, (

            data.get("brand"),

            data.get("model"),

            data.get("machine_type"),

            data.get("category"),

            data.get("capacity"),

            data.get("fuel_type"),

            data.get("voltage"),

            data.get("phase"),

            data.get("frequency"),

            data.get("manufacturer"),

            data.get("country"),

            data.get("manual_file"),

            data.get("image_file"),

            data.get("description"),

        ))

    # ==========================================================
    # Update
    # ==========================================================

    def update(self, machine_id, data):

        sql = """
        UPDATE machine_master
        SET

            brand=?,

            model=?,

            machine_type=?,

            category=?,

            capacity=?,

            fuel_type=?,

            voltage=?,

            phase=?,

            frequency=?,

            manufacturer=?,

            country=?,

            manual_file=?,

            image_file=?,

            description=?,

            updated_at=CURRENT_TIMESTAMP

        WHERE id=?
        """

        self.execute(sql, (

            data.get("brand"),

            data.get("model"),

            data.get("machine_type"),

            data.get("category"),

            data.get("capacity"),

            data.get("fuel_type"),

            data.get("voltage"),

            data.get("phase"),

            data.get("frequency"),

            data.get("manufacturer"),

            data.get("country"),

            data.get("manual_file"),

            data.get("image_file"),

            data.get("description"),

            machine_id,

        ))

    # ==========================================================
    # Delete
    # ==========================================================

    def delete(self, machine_id):

        self.execute("""
            DELETE FROM machine_master
            WHERE id = ?
        """, (machine_id,))


machine_master_repository = MachineMasterRepository()