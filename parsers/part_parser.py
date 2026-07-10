import re

# Part Number ของ IMAGE
PART_PATTERN = re.compile(r"A\d-[A-Z]\d{3}-\d{3}")

def extract_parts(text: str):

    lines = [x.strip() for x in text.splitlines() if x.strip()]

    parts = []

    i = 0

    while i < len(lines):

        # -----------------------
        # Item
        # -----------------------
        if lines[i].isdigit():

            item = lines[i]

            # -----------------------
            # Part Number
            # -----------------------
            if i + 1 < len(lines):

                if PART_PATTERN.fullmatch(lines[i + 1]):

                    part_no = lines[i + 1]

                    qty = ""

                    description = ""

                    # -----------------------
                    # Qty
                    # -----------------------
                    if i + 2 < len(lines):

                        if lines[i + 2].isdigit():

                            qty = lines[i + 2]

                            if i + 3 < len(lines):

                                description = lines[i + 3]

                    parts.append({

                        "item": item,
                        "part_no": part_no,
                        "qty": qty,
                        "description": description

                    })

        i += 1

    return parts