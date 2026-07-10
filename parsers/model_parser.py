import re

MODEL_PATTERNS = [
    r"IM\d+X\d+X\d+",
    r"SI\d+",
    r"DI\d+",
    r"DP\d+",
    r"SL\d+(?:-\d+)?",
    r"SP\d+",
    r"XD\d+",
    r"X-?DRYER\s?\d+",
]

DOCUMENT_PATTERNS = [
    r"DI\d{4}",
    r"DP\d{4}",
    r"XD\d{4}",
    r"IM\d{4}",
]


def extract_model(text: str):

    text = text.upper().replace("\n", " ")

    # -----------------------------
    # ลบเลข Document ออกก่อน
    # -----------------------------
    for pattern in DOCUMENT_PATTERNS:
        text = re.sub(pattern, " ", text)

    # -----------------------------
    # หา Model
    # -----------------------------
    for pattern in MODEL_PATTERNS:

        m = re.search(pattern, text)

        if m:

            return m.group(0)

    return "UNKNOWN"