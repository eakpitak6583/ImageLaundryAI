"""
LaundryBot V7 Enterprise
Dashboard Service
"""

import logging

from repositories.dashboard_repository import (
    dashboard_repository,
)

logger = logging.getLogger(

    __name__,

)


class DashboardService:

    def __init__(

        self,

    ):

        self.repo = dashboard_repository

        logger.info(

            "Dashboard Service Initialized"

        )

    # ==========================================================
    # Summary
    # ==========================================================

    def summary(

        self,

    ):

        logger.info(

            "Loading dashboard summary..."

        )

        try:

            summary = {

                "customer_total": self.repo.customer_count(),

                "machine_total": self.repo.machine_count(),

                "repair_total": self.repo.repair_count(),

                "repair_today": self.repo.today_repair(),

                "part_total": self.repo.part_count(),

                "document_total": self.repo.document_count(),

                "technician_total": self.repo.technician_count(),

            }

            logger.info(

                "Dashboard summary loaded successfully."

            )

            return summary

        except Exception as e:

            logger.exception(

                "Failed to load dashboard summary: %s",

                e,

            )

            return {

                "customer_total": 0,

                "machine_total": 0,

                "repair_total": 0,

                "repair_today": 0,

                "part_total": 0,

                "document_total": 0,

                "technician_total": 0,

            }


# ==========================================================
# Singleton
# ==========================================================

dashboard_service = DashboardService()