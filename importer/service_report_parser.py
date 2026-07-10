"""
LaundryBot V6

Service Report Parser
"""

import re

from importer.parsers.customer_parser import parse_customer
from importer.parsers.machine_parser import parse_machine
from importer.parsers.technician_parser import parse_technician
from importer.parsers.date_parser import parse_date
from importer.parsers.status_parser import parse_status


# ==========================================================
# Helper
# ==========================================================

def clean(text):

    text = text.replace("\r", "")

    return text


def extract(pattern, text):

    m = re.search(
        pattern,
        text,
        re.I | re.S
    )

    if m:

        return " ".join(

            m.group(1).split()

        )

    return ""


# ==========================================================
# Job
# ==========================================================

def parse_job(text):

    return extract(

        r"(JOB\d{4}-\d+)",

        text

    )


# ==========================================================
# Contact
# ==========================================================

def parse_contact(text):

    return extract(

        r"Contact\s+(.*?)\s+Location",

        text

    )


# ==========================================================
# Location
# ==========================================================

def parse_location(text):

    return extract(

        r"Location\s+(.*?)\s+Case Owner",

        text

    )


# ==========================================================
# Address
# ==========================================================

def parse_address(text):

    return extract(

        r"Address\s+(.*?)\s+Created By",

        text

    )


# ==========================================================
# Repair
# ==========================================================

def parse_repair(text):

    data = {}

    data["problem"] = extract(

        r"Problem\s+(.*?)\s+Repair",

        text

    )

    data["solution"] = extract(

        r"Repair(?: Action)?\s+(.*?)\s+Result",

        text

    )

    data["result"] = extract(

        r"Result\s+(.*)",

        text

    )

    return data


# ==========================================================
# Main
# ==========================================================

def parse(text):

    text = clean(text)

    data = {}

    # ----------------------------------------
    # Job
    # ----------------------------------------

    data["job_no"] = parse_job(text)

    # ----------------------------------------
    # Customer
    # ----------------------------------------

    data["customer"] = parse_customer(text)

    # ----------------------------------------
    # Contact
    # ----------------------------------------

    data["contact"] = parse_contact(text)

    # ----------------------------------------
    # Location
    # ----------------------------------------

    data["location"] = parse_location(text)

    # ----------------------------------------
    # Address
    # ----------------------------------------

    data["address"] = parse_address(text)

    # ----------------------------------------
    # Technician
    # ----------------------------------------

    data["case_owner"] = parse_technician(text)

    # ----------------------------------------
    # Machine
    # ----------------------------------------

    data.update(

        parse_machine(text)

    )

    # ----------------------------------------
    # Date
    # ----------------------------------------

    data.update(

        parse_date(text)

    )

    # ----------------------------------------
    # Status
    # ----------------------------------------

    data["status"] = parse_status(text)

    # ----------------------------------------
    # Repair
    # ----------------------------------------

    data.update(

        parse_repair(text)

    )

    return data