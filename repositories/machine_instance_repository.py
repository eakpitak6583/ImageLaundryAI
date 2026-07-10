from repositories.base_repository import BaseRepository


class MachineInstanceRepository(BaseRepository):

    def get_all(self):
        return self.fetch_all("""
            SELECT *
            FROM machine_instances
            ORDER BY serial_no
        """)

    def get(self, instance_id):
        return self.fetch_one("""
            SELECT *
            FROM machine_instances
            WHERE id = ?
        """, (instance_id,))

    def get_by_customer(self, customer_id):
        return self.fetch_all("""
            SELECT *
            FROM machine_instances
            WHERE customer_id = ?
        """, (customer_id,))