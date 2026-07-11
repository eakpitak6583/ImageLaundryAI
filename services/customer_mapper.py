"""
LaundryBot V7 Enterprise
Customer Mapper
"""

import re

from repositories.customer_repository import (
    customer_repository,
)


class CustomerMapper:

    def clean(self, text):

        if text is None:
            return ""

        text = text.strip()

        text = re.sub(r"\s+", " ", text)

        return text

    def normalize(self, customer):

        customer = self.clean(customer)

        alias = {

            "รพ.รามา": "โรงพยาบาลรามาธิบดี",
            "รามา": "โรงพยาบาลรามาธิบดี",

            "รพ.ศิริราช": "โรงพยาบาลศิริราช",
            "ศิริราช": "โรงพยาบาลศิริราช",

            "จุฬา": "โรงพยาบาลจุฬาลงกรณ์",

        }

        return alias.get(customer, customer)

    def find_or_create(self, customer):

        customer = self.normalize(customer)

        if customer == "":
            return None

        return customer_repository.find_or_create(
            customer
        )

    def mapping(self, ai_result):

        customer = ai_result.get(
            "customer",
            "",
        )

        customer_id = self.find_or_create(
            customer
        )

        return {

            "customer_id": customer_id,

            "customer_name": self.normalize(customer),

        }


customer_mapper = CustomerMapper()