"""
LaundryBot V7 Enterprise
Manual Service
"""

from repositories import manual_repository
from services.base_service import BaseService


class ManualService(BaseService):

    def __init__(self):

        self.repo = manual_repository

    def get_all(self):
        return self.repo.get_all()

    def get(self, manual_id):
        return self.repo.get(manual_id)

    def get_by_model(self, model):
        return self.repo.get_by_model(model)

    def search(self, keyword):
        return self.repo.search(keyword)

    def create(self, data):

        if not data.get("model"):
            return self.error("Model is required")

        manual_id = self.repo.create(data)

        return self.success(manual_id)

    def update(self, manual_id, data):

        self.repo.update(manual_id, data)

        return self.success()

    def delete(self, manual_id):

        self.repo.delete(manual_id)

        return self.success()


manual_service = ManualService()