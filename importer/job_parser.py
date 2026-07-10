"""
LaundryBot V6

Job Parser
"""

import re


def find(pattern, text):

    m = re.search(pattern, text, re.S | re.I)

    if m:
        return m.group(1).strip()

    return ""


def parse_job(lines):

    text = "\n".join(lines)

    data = {}

    # ------------------------------------
    # JOB
    # ------------------------------------

    m = re.search(r"(JOB\d{4}-\d+)", text)

    data["job_no"] = m.group(1) if m else ""

    # ------------------------------------
    # Complaint
    # ------------------------------------

    data["problem"] = find(

        r"Complaint\s*:\s*(.*?)\nDetail",

        text

    )

    # ------------------------------------
    # Detail
    # ------------------------------------

    data["detail"] = find(

        r"Detail\s*:\s*(.*?)(?:Team|ผลชปฏรบษตรงาน|$)",

        text

    )

    # ------------------------------------
    # Solution
    # ------------------------------------

    data["solution"] = find(

        r"ดจาเนรนการแกชไข\s*:\s*(.*?)ผลการแกชไข",

        text

    )

    # ------------------------------------
    # Result
    # ------------------------------------

    data["result"] = find(

        r"ผลการแกชไข\s*:\s*(.*?)Complaint",

        text

    )

    # ------------------------------------
    # Machine Model
    # ------------------------------------

    model = re.search(

        r"(SB-\d+|SI-\d+|DI-\d+|HC-\d+|XPS\d+/\d+|XT-\w+|X-Dryer120|AMFOLD-\w+|IM\d+x\d+x\d+)",

        text,

        re.I

    )

    data["machine_model"] = model.group(1) if model else ""

    # ------------------------------------
    # SAP
    # ------------------------------------

    sap = re.search(

        r"SAP\s*([0-9]{8,})",

        text

    )

    data["sap_no"] = sap.group(1) if sap else ""

    # ------------------------------------
    # Serial Number
    # ------------------------------------

    sn = re.search(

        r"S/N[: ]*([A-Z0-9\/\-]+)",

        text,

        re.I

    )

    data["serial"] = sn.group(1) if sn else ""

    return data