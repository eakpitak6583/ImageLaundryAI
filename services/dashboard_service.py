"""
LaundryBot V7 Enterprise
Dashboard Service
"""

from repositories.dashboard_repository import dashboard_repository


class DashboardService:

    def __init__(self):

        self.repo = dashboard_repository

    def summary(self):

        return {

            "customer_total": self.repo.customer_count(),

            "machine_total": self.repo.machine_count(),

            "repair_total": self.repo.repair_count(),

            "repair_today": self.repo.today_repair(),

            "part_total": self.repo.part_count(),

            "document_total": self.repo.document_count(),

            "technician_total": self.repo.technician_count(),

        }


dashboard_service = DashboardService()