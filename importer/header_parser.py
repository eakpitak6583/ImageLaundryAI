"""
LaundryBot V6

Header Parser
"""

import re


def find(pattern, text):

    m = re.search(pattern, text, re.I | re.S)

    if m:
        return m.group(1).strip()

    return ""


def parse_header(text):

    data = {}

    # ----------------------------
    # Customer
    # ----------------------------

    data["customer"] = find(

        r"Customer\s*(.*?)\s*Contact",

        text

    )

    if not data["customer"]:

        data["customer"] = find(

            r"ลูกค้า\s*:?\s*(.*?)\s*(?:JOB\d{4}|วันที่เอกสาร|Complaint)",

            text

        )

    # ----------------------------
    # Contact
    # ----------------------------

    data["contact"] = find(

        r"Contact\s*(.*?)\s*Location",

        text

    )

    # ----------------------------
    # Case Owner
    # ----------------------------

    data["case_owner"] = find(

        r"Case Owner\s*(.*?)\s*Address",

        text

    )

    return data