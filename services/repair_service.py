"""
Image Laundry AI
Repair Service
"""

from repositories.repair_repository import (
    repair_repository,
)

from services.base_service import BaseService
from services.repair_ai_service import (
    repair_ai_service,
)


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

    # ==========================================================
    # Create
    # ==========================================================

    def create(self, data):

        if not data.get("job_no"):

            return self.error(
                "Job No is required"
            )

        if not data.get("machine_id"):

            return self.error(
                "Machine is required"
            )

        if not data.get("customer_id"):

            return self.error(
                "Customer is required"
            )

        if not data.get("technician_id"):

            return self.error(
                "Technician is required"
            )

        if not data.get("complaint"):

            return self.error(
                "Complaint is required"
            )

        repair_id = self.repo.create(data)

        return self.success(repair_id)
    # ==========================================================
    # AI Import PDF
    # ==========================================================

    def import_pdf(self, filepath):

        result = repair_ai_service.import_pdf(
            filepath
        )

        repair_id = self.repo.create_ai(
            result
        )

        return {

            "success": True,

            "repair_id": repair_id,

            "data": result,

        }
    # ==========================================================
    # Update
    # ==========================================================

    def update(self, repair_id, data):

        repair = self.repo.get(repair_id)

        if not repair:

            return self.error(
                "Repair not found"
            )

        self.repo.update(
            repair_id,
            data,
        )

        return self.success()

    # ==========================================================
    # Delete
    # ==========================================================

    def delete(self, repair_id):

        repair = self.repo.get(repair_id)

        if not repair:

            return self.error(
                "Repair not found"
            )

        self.repo.delete(
            repair_id
        )

        return self.success()

    # ==========================================================
    # Dashboard
    # ==========================================================

    def latest(self, limit=10):

        repairs = self.repo.get_all()

        return repairs[:limit]


repair_service = RepairService()
    # ==========================================================
    # Statistics
    # ==========================================================

    def total(self):

        return self.repo.total()

    def top_machine(self, limit=10):

        return self.repo.top_machine(limit)

    def top_complaint(self, limit=10):

        return self.repo.top_complaint(limit)