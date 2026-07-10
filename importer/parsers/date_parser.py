"""
LaundryBot V6

Date Parser
"""

import re


def find(pattern, text):

    m = re.search(pattern, text, re.I | re.S)

    if m:
        return m.group(1).strip()

    return ""


def parse_date(text):

    data = {}

    # ==========================================
    # Document Date
    # ==========================================

    data["document_date"] = find(

        r"Document Date\s*([0-9]{2}/[0-9]{2}/[0-9]{4})",

        text

    )

    if not data["document_date"]:

        data["document_date"] = find(

            r"วันที่เอกสาร\s*([0-9]{2}/[0-9]{2}/[0-9]{4})",

            text

        )

    # ==========================================
    # Receive Date
    # ==========================================

    data["receive_date"] = find(

        r"วันที่รับงาน\s*([0-9]{2}/[0-9]{2}/[0-9]{4})",

        text

    )

    # ==========================================
    # Finish Date
    # ==========================================

    data["finish_date"] = find(

        r"วันที่จบงาน\s*([0-9]{2}/[0-9]{2}/[0-9]{4})",

        text

    )

    # ==========================================
    # Start Time
    # ==========================================

    data["start_time"] = find(

        r"วันที่รับงาน.*?([0-9]{2}:[0-9]{2})",

        text

    )

    # ==========================================
    # Finish Time
    # ==========================================

    data["finish_time"] = find(

        r"วันที่จบงาน.*?([0-9]{2}:[0-9]{2})",

        text

    )

    return data