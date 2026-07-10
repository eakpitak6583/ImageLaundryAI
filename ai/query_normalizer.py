SYNONYMS = {
    "สตีม": "steam",
    "ไอน้ำ": "steam",
    "โซลินอยด์": "solenoid",
    "โซลินอยด์วาล์ว": "solenoid valve",
    "คอยล์": "coil",
    "มอเตอร์": "motor",
    "ลูกปืน": "bearing",
    "สายพาน": "belt",
}


def normalize_question(question: str):

    q = question.lower()

    for old, new in SYNONYMS.items():
        q = q.replace(old.lower(), new.lower())

    return q