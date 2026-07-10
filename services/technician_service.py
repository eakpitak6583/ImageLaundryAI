"""
LaundryBot V7 Enterprise
Technician Service
"""

from repositories import technician_repository
from services.base_service import BaseService


class TechnicianService(BaseService):

    def __init__(self):

        self.repo = technician_repository

    # ==========================================================

    def get_all(self):
        return self.repo.get_all()

    def get(self, technician_id):
        return self.repo.get(technician_id)

    def search(self, keyword):
        return self.repo.search(keyword)

    # ==========================================================

    def create(self, data):

        if not data.get("fullname"):
            return self.error("Technician name is required")

        technician_id = self.repo.create(data)

        return self.success(technician_id)

    # ==========================================================

    def update(self, technician_id, data):

        self.repo.update(technician_id, data)

        return self.success()

    # ==========================================================

    def delete(self, technician_id):

        self.repo.delete(technician_id)

        return self.success()


technician_service = TechnicianService()