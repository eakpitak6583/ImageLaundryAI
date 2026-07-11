"""
LaundryBot V7 Enterprise
Technician Mapper
"""

import re

from repositories.technician_repository import (
    technician_repository,
)


class TechnicianMapper:

    def __init__(self):

        self.alias = {

            "ช.": "",

            "นาย": "",

            "Mr.": "",

            "MR.": "",

        }

    # =====================================================
    # Clean
    # =====================================================

    def clean(self, text):

        if text is None:

            return ""

        text = text.strip()

        text = re.sub(

            r"\s+",

            " ",

            text,

        )

        return text

    # =====================================================
    # Normalize
    # =====================================================

    def normalize(self, name):

        name = self.clean(name)

        if name == "":

            return ""

        for k, v in self.alias.items():

            name = name.replace(

                k,

                v,

            )

        return name.strip()

    # =====================================================
    # Find or Create
    # =====================================================

    def find_or_create(

        self,

        technician,

        employee_code="",

    ):

        technician = self.normalize(

            technician

        )

        if technician == "":

            return None

        return technician_repository.find_or_create(

            name=technician,

            employee_code=employee_code,

        )

    # =====================================================
    # Mapping
    # =====================================================

    def mapping(

        self,

        ai_result,

    ):

        technician = ai_result.get(

            "technician",

            "",

        )

        employee_code = ai_result.get(

            "employee_code",

            "",

        )

        technician_id = self.find_or_create(

            technician,

            employee_code,

        )

        return {

            "technician_id": technician_id,

            "technician_name": self.normalize(

                technician

            ),

        }


technician_mapper = TechnicianMapper()