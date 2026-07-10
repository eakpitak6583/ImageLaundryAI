"""
Image Laundry AI
Customer Service
"""

from repositories.customer_repository import (
    customer_repository,
)

from services.base_service import BaseService


class CustomerService(BaseService):

    def __init__(self):

        self.repo = customer_repository

    # ==========================================================
    # Read
    # ==========================================================

    def get_all(self):

        return self.repo.get_all()

    def get(self, customer_id):

        return self.repo.get(customer_id)

    def search(self, keyword):

        return self.repo.search(keyword)

    # ==========================================================
    # Create
    # ==========================================================

    def create(self, data):

        if not data.get("name"):

            return self.error(
                "Customer Name is required"
            )

        customer_id = self.repo.create(data)

        return self.success(customer_id)

    # ==========================================================
    # Update
    # ==========================================================

    def update(self, customer_id, data):

        self.repo.update(
            customer_id,
            data,
        )

        return self.success()

    # ==========================================================
    # Delete
    # ==========================================================

    def delete(self, customer_id):

        self.repo.delete(customer_id)

        return self.success()


customer_service = CustomerService()