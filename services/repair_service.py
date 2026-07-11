"""
LaundryBot V7 Enterprise
Repair Service
"""

import logging

from repositories.repair_repository import (
    repair_repository,
)

from services.base_service import (
    BaseService,
)

from services.repair_ai_service import (
    repair_ai_service,
)


logger = logging.getLogger(

    __name__,

)


class RepairService(BaseService):

    # ==========================================================
    # Constructor
    # ==========================================================

    def __init__(

        self,

    ):

        super().__init__()

        self.repo = repair_repository

        logger.info(

            "Repair Service Initialized"

        )

    # ==========================================================
    # Read
    # ==========================================================

    def get_all(

        self,

    ):

        return self.repo.get_all()

    def get(

        self,

        repair_id,

    ):

        return self.repo.get(

            repair_id,

        )

    def search(

        self,

        keyword,

    ):

        return self.repo.search(

            keyword,

        )

    def get_by_machine(

        self,

        machine_id,

    ):

        return self.repo.get_by_machine(

            machine_id,

        )

    # ==========================================================
    # Create
    # ==========================================================
    def create(

        self,

        data,

    ):

        logger.info(

            "Creating repair record..."

        )

        required_fields = [

            "machine_id",

            "customer_id",

            "technician_id",

            "complaint",

        ]

        for field in required_fields:

            value = data.get(

                field,

                "",

            )

            if value is None:

                value = ""

            value = str(

                value,

            ).strip()

            if value == "":

                return self.error(

                    f"{field} is required"

                )

        repair_id = self.repo.create(

            data,

        )

        logger.info(

            "Repair ID : %s",

            repair_id,

        )

        return {

            "success": True,

            "repair_id": repair_id,

            "data": repair_id,

        }

    # ==========================================================
    # AI Import PDF
    # ==========================================================

    def import_pdf(

        self,

        filepath,

    ):

        logger.info(

            "AI Import Started : %s",

            filepath,

        )

        result = repair_ai_service.safe_import(

            filepath,

        )

        repair_id = self.repo.create_ai(

            result,

        )

        logger.info(

            "AI Import Completed : %s",

            repair_id,

        )

        return {

            "success": True,

            "repair_id": repair_id,

            "data": result,

        }

    # ==========================================================
    # Update
    # ==========================================================
    def update(

        self,

        repair_id,

        data,

    ):

        logger.info(

            "Updating repair : %s",

            repair_id,

        )

        repair = self.repo.get(

            repair_id,

        )

        if repair is None:

            return self.error(

                "Repair not found"

            )

        self.repo.update(

            repair_id,

            data,

        )

        logger.info(

            "Repair updated : %s",

            repair_id,

        )

        return self.success()

    # ==========================================================
    # Delete
    # ==========================================================

    def delete(

        self,

        repair_id,

    ):

        logger.info(

            "Deleting repair : %s",

            repair_id,

        )

        repair = self.repo.get(

            repair_id,

        )

        if repair is None:

            return self.error(

                "Repair not found"

            )

        self.repo.delete(

            repair_id,

        )

        logger.info(

            "Repair deleted : %s",

            repair_id,

        )

        return self.success()

    # ==========================================================
    # Dashboard
    # ==========================================================

    def latest(

        self,

        limit=10,

    ):

        repairs = self.repo.get_all()

        return repairs[:limit]

    # ==========================================================
    # Statistics
    # ==========================================================
    def total(

        self,

    ):

        return self.repo.total()

    # ==========================================================
    # Top Machine
    # ==========================================================

    def top_machine(

        self,

        limit=10,

    ):

        return self.repo.top_machine(

            limit,

        )

    # ==========================================================
    # Top Customer
    # ==========================================================

    def top_customer(

        self,

        limit=10,

    ):

        return self.repo.top_customer(

            limit,

        )

    # ==========================================================
    # Top Technician
    # ==========================================================

    def top_technician(

        self,

        limit=10,

    ):

        return self.repo.top_technician(

            limit,

        )

    # ==========================================================
    # Top Complaint
    # ==========================================================

    def top_complaint(

        self,

        limit=10,

    ):

        return self.repo.top_complaint(

            limit,

        )

    # ==========================================================
    # Singleton
    # ==========================================================
        repair_service = RepairService()