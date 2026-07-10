"""
LaundryBot V5

PDF Parser
"""

import re


def get_value(label, text):

    pattern = rf"{label}\s*:?\s*(.+)"

    m = re.search(
        pattern,
        text,
        re.IGNORECASE,
    )

    if m:

        return m.group(1).strip()

    return ""


def parse(text):

    data = {

        "job_no":

            get_value(
                "Job No",
                text,
            ),

        "customer":

            get_value(
                "Customer",
                text,
            ),

        "engineer":

            get_value(
                "Engineer",
                text,
            ),

        "machine":

            get_value(
                "Machine",
                text,
            ),

        "serial":

            get_value(
                "Serial",
                text,
            ),

        "problem":

            get_value(
                "Problem",
                text,
            ),

        "solution":

            get_value(
                "Solution",
                text,
            ),

        "result":

            get_value(
                "Result",
                text,
            ),

    }

    return data