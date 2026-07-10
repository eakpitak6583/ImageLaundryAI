"""
LaundryBot V7 Enterprise
Customer Service
"""

from repositories import customer_repository
from services.base_service import BaseService


class CustomerService(BaseService):

    def __init__(self):

        self.repo = customer_repository

    # ==========================================================

    def get_all(self):
        return self.repo.get_all()

    def get(self, customer_id):
        return self.repo.get(customer_id)

    def search(self, keyword):
        return self.repo.search(keyword)

    # ==========================================================

    def create(self, data):

        if not data.get("customer_name"):
            return self.error("Customer Name is required")

        customer_id = self.repo.create(data)

        return self.success(customer_id)

    # ==========================================================

    def update(self, customer_id, data):

        self.repo.update(customer_id, data)

        return self.success()

    # ==========================================================

    def delete(self, customer_id):

        self.repo.delete(customer_id)

        return self.success()


customer_service = CustomerService()