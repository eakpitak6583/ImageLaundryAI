"""
LaundryBot V6

Status Parser
"""

import re


def parse_status(text):

    status = ""

    patterns = [

        r"\b(Finish)\b",

        r"\b(Inprogress)\b",

        r"\b(Pending)\b",

        r"\b(Cancel)\b",

    ]

    for pattern in patterns:

        m = re.search(pattern, text, re.I)

        if m:

            status = m.group(1)

            break

    return status