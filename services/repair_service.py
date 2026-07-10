"""
LaundryBot V7 Enterprise
Repair Service
"""

from repositories import repair_repository
from services.base_service import BaseService


class RepairService(BaseService):

    def __init__(self):
        self.repo = repair_repository

    # ==========================================================
    # Read
    # ==========================================================

    def get_all(self):
        return self.repo.get_all()

    def get(self, repair_id):
        return self.repo.get(repair_id)

    def search(self, keyword):
        return self.repo.search(keyword)

    def get_by_machine(self, machine_id):
        return self.repo.get_by_machine(machine_id)

    def get_by_customer(self, customer_id):
        return self.repo.get_by_customer(customer_id)

    def get_by_technician(self, technician_id):
        return self.repo.get_by_technician(technician_id)

    # ==========================================================
    # Create
    # ==========================================================

    def create(self, data):

        required_fields = [
            "job_no",
            "machine_id",
            "customer_id",
            "technician_id",
            "complaint",
        ]

        for field in required_fields:
            if not data.get(field):
                return self.error(f"{field} is required")

        repair_id = self.repo.create(data)

        return self.success(repair_id)

    # ==========================================================
    # Update
    # ==========================================================

    def update(self, repair_id, data):

        if not self.repo.get(repair_id):
            return self.error("Repair not found")

        self.repo.update(repair_id, data)

        return self.success(repair_id)

    # ==========================================================
    # Delete
    # ==========================================================

    def delete(self, repair_id):

        if not self.repo.get(repair_id):
            return self.error("Repair not found")

        self.repo.delete(repair_id)

        return self.success()

    # ==========================================================
    # Dashboard
    # ==========================================================

    def latest(self, limit=10):

        repairs = self.repo.get_all()

        return repairs[:limit]


repair_service = RepairService()