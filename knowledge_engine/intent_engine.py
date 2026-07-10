import re


PART_KEYWORDS = [

    "part",
    "part no",
    "part number",
    "spare",

    "อะไหล่",

]

MANUAL_KEYWORDS = [

    "manual",
    "คู่มือ",
    "diagram",
    "drawing",
    "wiring",

]

REPAIR_KEYWORDS = [

    "repair",
    "problem",
    "alarm",
    "error",

    "เสีย",
    "ไม่ทำงาน",
    "ไม่ร้อน",
    "ไม่หมุน",
    "ไม่เข้า",
    "steam",
    "น้ำ",

]


def detect_intent(question: str):

    q = question.lower().strip()

    for word in PART_KEYWORDS:

        if word in q:

            return {

                "intent": "parts",

                "keyword": question,

            }

    for word in MANUAL_KEYWORDS:

        if word in q:

            return {

                "intent": "manual",

                "keyword": question,

            }

    return {

        "intent": "repair",

        "keyword": question,

    }