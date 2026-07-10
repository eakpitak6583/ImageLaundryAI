import re

# =====================================================
# Section Keywords
# =====================================================

SECTION_MAP = {

    "complaint": [
        "PROBLEM",
        "REQUEST DETAIL",
        "REQUEST",
        "COMPLAINT",
        "ปัญหา",
        "อาการ",
        "รายละเอียดปัญหา",
    ],

    "detail": [
        "DETAIL",
        "DESCRIPTION",
        "รายละเอียด",
    ],

    "repair_action": [
        "SOLUTION",
        "CORRECTIVE ACTION",
        "ACTION",
        "REPAIR",
        "การแก้ไข",
        "วิธีแก้ไข",
        "ดำเนินการ",
    ],

    "result": [
        "RESULT",
        "STATUS",
        "FINISH",
        "ผลการซ่อม",
        "ผลการดำเนินงาน",
    ],
}


# =====================================================
# Clean Text
# =====================================================

def clean_text(text: str):

    return " ".join(text.replace("\r", "").split())


# =====================================================
# Regex
# =====================================================

def find(pattern, text):

    match = re.search(
        pattern,
        text,
        re.IGNORECASE,
    )

    if not match:
        return ""

    if match.lastindex:
        return clean_text(match.group(1))

    return clean_text(match.group(0))


# =====================================================
# Extract Section
# =====================================================

def extract_section(text, starts):

    upper = text.upper()

    start_pos = -1

    for word in starts:

        pos = upper.find(word.upper())

        if pos != -1:
            start_pos = pos + len(word)
            break

    if start_pos == -1:
        return ""

    end_pos = len(text)

    for group in SECTION_MAP.values():

        for word in group:

            pos = upper.find(word.upper(), start_pos)

            if pos != -1:

                end_pos = min(
                    end_pos,
                    pos,
                )

    return clean_text(
        text[start_pos:end_pos]
    )


# =====================================================
# Main Parser
# =====================================================

def extract_service_data(text):

    text = text.replace("\x00", "")

    data = {

        "job_no": "",

        "machine_model": "",

        "serial_no": "",

        "sap_no": "",

        "complaint": "",

        "detail": "",

        "repair_action": "",

        "result": "",

    }

    # ---------------------------------
    # Job Number
    # ---------------------------------

    data["job_no"] = find(

        r"(JOB\d{4}-\d+)",

        text,

    )

    # ---------------------------------
    # Machine Model
    # ---------------------------------

    data["machine_model"] = find(

        r"MODEL\s*:?([^\n]+)",

        text,

    )

    # ---------------------------------
    # Serial Number
    # ---------------------------------

    data["serial_no"] = find(

        r"SERIAL\s*(?:NO\.?|NUMBER)?\s*:?([^\n]+)",

        text,

    )

    # ---------------------------------
    # SAP Number
    # ---------------------------------

    data["sap_no"] = find(

        r"SAP\s*(?:NO\.?)?\s*:?([^\n]+)",

        text,

    )

    # ---------------------------------
    # Complaint
    # ---------------------------------

    data["complaint"] = extract_section(

        text,

        SECTION_MAP["complaint"],

    )

    # ---------------------------------
    # Detail
    # ---------------------------------

    data["detail"] = extract_section(

        text,

        SECTION_MAP["detail"],

    )

    # ---------------------------------
    # Repair Action
    # ---------------------------------

    data["repair_action"] = extract_section(

        text,

        SECTION_MAP["repair_action"],

    )

    # ---------------------------------
    # Result
    # ---------------------------------

    data["result"] = extract_section(

        text,

        SECTION_MAP["result"],

    )

    return data