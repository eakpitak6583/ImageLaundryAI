"""
LaundryBot V6

Machine Parser
"""

import re


def find(pattern, text):

    m = re.search(pattern, text, re.I | re.S)

    if m:
        return m.group(1).strip()

    return ""


def parse_machine(text):

    data = {}

    # =====================================================
    # Machine Model
    # =====================================================

    patterns = [

        r"(DI-\d+)",
        r"(SP-\d+)",
        r"(SB-\d+)",
        r"(HC-\d+)",
        r"(XT-[A-Z0-9/.-]+)",
        r"(X-Dryer\d+)",
        r"(VEGA\s*DP\d+)",
        r"(IM\d+X\d+X\d+)",

    ]

    data["machine_model"] = ""

    for p in patterns:

        m = re.search(p, text, re.I)

        if m:

            data["machine_model"] = m.group(1)

            break

    # =====================================================
    # SAP
    # =====================================================

    sap = re.search(

        r"SAP[: ]*([0-9]{8,})",

        text,

        re.I

    )

    data["sap_no"] = sap.group(1) if sap else ""

    # =====================================================
    # Serial
    # =====================================================

    serial = re.search(

        r"S/N[: ]*([A-Z0-9/\-]+)",

        text,

        re.I

    )

    data["serial"] = serial.group(1) if serial else ""

    return data