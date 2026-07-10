from pathlib import Path


MANUAL_KEYWORDS = [
    "table of contents",
    "installation",
    "maintenance",
    "troubleshooting",
    "spare parts",
    "parts list",
]

SERVICE_KEYWORDS = [
    "complaint",
    "repair",
    "corrective action",
    "service report",
    "result",
]


def classify_document(filename: str, text: str):

    lower = (filename + " " + text).lower()

    manual_score = 0
    service_score = 0

    for word in MANUAL_KEYWORDS:

        if word in lower:
            manual_score += 1

    for word in SERVICE_KEYWORDS:

        if word in lower:
            service_score += 1

    if service_score > manual_score:
        return "service_report"

    return "manual"