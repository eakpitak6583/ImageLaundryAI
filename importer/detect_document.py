"""
LaundryBot V6

Detect Document Type
"""


def detect_document(text):

    t = text.lower()

    # ======================================================
    # Service Control Order
    # ======================================================

    if (
        "service control" in t
        or "service control order" in t
        or "customer signature" in t
    ):

        return "service_report"

    # ======================================================
    # Summary Report
    # ======================================================

    summary_keywords = [

        "complaint :",
        "detail :",
        "ผลการแก้ไข",
        "ดำเนินการแก้ไข",
        "ตรวจสอบเบื้องต้น",
        "team",
        "finish",
        "job690",
        "job691",

    ]

    score = 0

    for k in summary_keywords:

        if k.lower() in t:

            score += 1

    if score >= 3:

        return "summary_report"

    # ======================================================
    # Parts Manual
    # ======================================================

    if (

        "parts list" in t

        or "part no." in t

        or "section" in t

    ):

        return "parts_manual"

    return "unknown"