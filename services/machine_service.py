"""
LaundryBot V7 Enterprise
Machine Service
"""

from repositories import machine_repository
from services.base_service import BaseService


class MachineService(BaseService):

    def __init__(self):

        self.repo = machine_repository

    # ==========================================================

    def get_all(self):

        return self.repo.get_all()

    def get(self, machine_id):

        return self.repo.get(machine_id)

    def search(self, keyword):

        return self.repo.search(keyword)

    # ==========================================================

    def create(self, data):

        if not data.get("brand"):
            return self.error("Brand is required")

        if not data.get("model"):
            return self.error("Model is required")

        machine_id = self.repo.create(data)

        return self.success(machine_id)

    # ==========================================================

    def update(self, machine_id, data):

        self.repo.update(machine_id, data)

        return self.success()

    # ==========================================================

    def delete(self, machine_id):

        self.repo.delete(machine_id)

        return self.success()


machine_service = MachineService()