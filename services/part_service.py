"""
LaundryBot V7 Enterprise
Part Service
"""

from repositories import part_repository
from services.base_service import BaseService


class PartService(BaseService):

    def __init__(self):

        self.repo = part_repository

    def get_all(self):
        return self.repo.get_all()

    def get(self, part_id):
        return self.repo.get(part_id)

    def get_by_model(self, model):
        return self.repo.get_by_model(model)

    def search(self, keyword):
        return self.repo.search(keyword)

    def create(self, data):

        if not data.get("part_no"):
            return self.error("Part Number is required")

        return self.success(
            self.repo.create(data)
        )

    def update(self, part_id, data):

        self.repo.update(part_id, data)

        return self.success()

    def delete(self, part_id):

        self.repo.delete(part_id)

        return self.success()


part_service = PartService()