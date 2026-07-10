"""
LaundryBot V6

Summary Report Parser
"""

import re

from importer.header_parser import parse_header


# ==========================================================
# Helper
# ==========================================================

def find(pattern, text):

    m = re.search(
        pattern,
        text,
        re.I | re.S
    )

    if m:
        return " ".join(m.group(1).split())

    return ""


# ==========================================================
# Parse Summary Report
# ==========================================================

def parse_summary(text):

    jobs = []

    header = parse_header(text)

    blocks = re.split(

        r"(?=JOB\d{4}-\d+)",

        text

    )

    for block in blocks:

        if "JOB" not in block:
            continue

        data = {

            "customer": header.get("customer", ""),
            "contact": header.get("contact", ""),
            "case_owner": header.get("case_owner", ""),

            "job_no": "",
            "problem": "",
            "detail": "",
            "solution": "",
            "result": "",

            "machine_model": "",
            "sap_no": "",
            "serial": "",

        }

        # =====================================================
        # JOB
        # =====================================================

        data["job_no"] = find(

            r"(JOB\d{4}-\d+)",

            block

        )

        # =====================================================
        # Complaint
        # =====================================================

        data["problem"] = find(

            r"Complaint\s*:\s*(.*?)(?:Detail\s*:|$)",

            block

        )

        # =====================================================
        # Detail
        # =====================================================

        data["detail"] = find(

            r"Detail\s*:\s*(.*?)(?:Team|ททมปฏ|$)",

            block

        )

        # =====================================================
        # Solution
        # =====================================================

        data["solution"] = find(

            r"ด[ำจ]าเนินการแก้ไข\s*:\s*(.*?)ผลการแก้ไข",

            block

        )

        # =====================================================
        # Result
        # =====================================================

        data["result"] = find(

            r"ผลการแก้ไข\s*:\s*(.*?)(?:Complaint|$)",

            block

        )

        # =====================================================
        # Machine Model
        # =====================================================

        model_patterns = [

            r"XT-[A-Z0-9/.-]+",
            r"XPS\d+/\d+",
            r"XPW\d+/\d+",
            r"X-Dryer\d+",
            r"DI-\d+",
            r"SP-\d+",
            r"SB-?\d+",
            r"SI-\d+",
            r"HC-\d+",
            r"AMFOLD-[A-Z]",
            r"IM\d+X\d+X\d+",
            r"VEGA",
            r"DP\d+",
            r"IMLP-[A-Z0-9]+",

        ]

        for pattern in model_patterns:

            m = re.search(

                pattern,

                block,

                re.I

            )

            if m:

                data["machine_model"] = m.group(0)

                break

        # =====================================================
        # SAP
        # =====================================================

        sap = re.search(

            r"SAP\s*([0-9]{8,})",

            block,

            re.I

        )

        if sap:

            data["sap_no"] = sap.group(1)

        # =====================================================
        # Serial
        # =====================================================

        serial = re.search(

            r"S\/N\s*[: ]*\s*([A-Z0-9/\-]+)",

            block,

            re.I

        )

        if serial:

            data["serial"] = serial.group(1)

        jobs.append(data)

    return jobs