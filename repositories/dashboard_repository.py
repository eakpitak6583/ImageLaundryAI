"""
Image Laundry AI
Dashboard Repository
"""

from repositories.base_repository import BaseRepository


class DashboardRepository(BaseRepository):

    # ==========================================================
    # Customers
    # ==========================================================

    def customer_count(self):

        row = self.fetch_one("""
            SELECT COUNT(*) AS total
            FROM customers
        """)

        return row["total"] if row else 0

    # ==========================================================
    # Machines
    # ==========================================================

    def machine_count(self):

        row = self.fetch_one("""
            SELECT COUNT(*) AS total
            FROM machines
        """)

        return row["total"] if row else 0

    # ==========================================================
    # Repairs
    # ==========================================================

    def repair_count(self):

        row = self.fetch_one("""
            SELECT COUNT(*) AS total
            FROM repair_history
        """)

        return row["total"] if row else 0

    def today_repair(self):

        row = self.fetch_one("""
            SELECT COUNT(*) AS total
            FROM repair_history
            WHERE DATE(created_at)=DATE('now','localtime')
        """)

        return row["total"] if row else 0

    # ==========================================================
    # Parts
    # ==========================================================

    def part_count(self):

        row = self.fetch_one("""
            SELECT COUNT(*) AS total
            FROM parts
        """)

        return row["total"] if row else 0

    # ==========================================================
    # Documents
    # ==========================================================

    def document_count(self):

        row = self.fetch_one("""
            SELECT COUNT(*) AS total
            FROM documents
        """)

        return row["total"] if row else 0

    # ==========================================================
    # Technicians
    # ==========================================================

    def technician_count(self):

        row = self.fetch_one("""
            SELECT COUNT(*) AS total
            FROM technicians
        """)

        return row["total"] if row else 0


dashboard_repository = DashboardRepository()