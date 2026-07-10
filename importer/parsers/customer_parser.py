"""
LaundryBot V6

Customer Parser
"""

import re


def parse_customer(text):

    patterns = [

        # Service Control Order
        r"Customer\s+(.*?)\s+Contact",

        # Summary Report
        r"ลลกคชา.*?\n(.*?)(?=\n\S|\Z)",

    ]

    for pattern in patterns:

        m = re.search(pattern, text, re.I | re.S)

        if m:

            customer = m.group(1)

            # ลบช่องว่างเกิน
            customer = " ".join(customer.split())

            # ตัดข้อความที่ไม่ใช่ชื่อลูกค้า
            customer = customer.replace(
                "acknowledgement, equipment work, spare parts and technician confirmation.",
                ""
            )

            customer = customer.replace(
                "Customer",
                ""
            )

            return customer.strip()

    return ""