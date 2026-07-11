"""
LaundryBot V7 Enterprise
Machine Mapper
"""

import re

from repositories.machine_repository import (
    machine_repository,
)


class MachineMapper:

    def clean(self, text):

        if text is None:
            return ""

        text = text.strip()

        text = re.sub(r"\s+", " ", text)

        return text

    def normalize_brand(self, brand):

        brand = self.clean(brand)

        return brand.upper()

    def normalize_model(self, model):

        model = self.clean(model)

        return model.upper()

    def mapping(

        self,

        ai_result,

        customer_id=None,

    ):

        brand = self.normalize_brand(

            ai_result.get("brand", "")

        )

        model = self.normalize_model(

            ai_result.get("machine_model", "")

        )

        sap = ai_result.get("sap_no", "")

        serial = ai_result.get("serial_no", "")

        machine_id = machine_repository.find_or_create(

            brand=brand,

            model=model,

            sap_no=sap,

            serial_no=serial,

            customer_id=customer_id,

        )

        return {

            "machine_id": machine_id,

            "brand": brand,

            "model": model,

        }


machine_mapper = MachineMapper()