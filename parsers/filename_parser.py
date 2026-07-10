import re

def parse_filename(filename: str):

    text = filename.upper()

    # IM1200X3300X3
    m = re.search(r"IM\d+X\d+X\d+", text)
    if m:
        return m.group(0)

    # DI475
    m = re.search(r"DI\d{3}(?!\d)", text)
    if m:
        return m.group(0)

    # DP250
    m = re.search(r"DP\d{3}(?!\d)", text)
    if m:
        return m.group(0)

    # SI275
    m = re.search(r"SI\d{3}(?!\d)", text)
    if m:
        return m.group(0)

    # SL400-3
    m = re.search(r"SL\d+(?:-\d+)?", text)
    if m:
        return m.group(0)

    # SP185
    m = re.search(r"SP\d{3}(?!\d)", text)
    if m:
        return m.group(0)

    # XD120
    m = re.search(r"XD\d{3}(?!\d)", text)
    if m:
        return m.group(0)

    # X-Dryer120
    m = re.search(r"X-?DRYER\s?\d+", text)
    if m:
        return m.group(0).replace(" ", "")

    return "UNKNOWN"