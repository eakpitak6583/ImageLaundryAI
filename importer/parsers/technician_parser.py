"""
LaundryBot V6

Technician Parser
"""

import re


def parse_technician(text):

    technician = ""

    patterns = [

        r"Case Owner\s+\[.*?\]\s*(.*?)\s+Address",

        r"Case Owner\s+(.*?)\s+Address",

        r"Technician\s*/\s*Date.*?\n(.*?)\n",

    ]

    for pattern in patterns:

        m = re.search(

            pattern,

            text,

            re.I | re.S

        )

        if m:

            technician = m.group(1).strip()

            technician = " ".join(

                technician.split()

            )

            break

    return technician