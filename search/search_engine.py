"""
LaundryBot V5

Central Search Engine

ทุก Module ต้องค้นหาผ่านไฟล์นี้
"""

from repositories.part_repository import search_parts as repo_parts
from repositories.manual_repository import search_manuals as repo_manuals
from repositories.repair_repository import search_repairs as repo_repairs


# ==========================================================
# Normalize Model
# ==========================================================

def normalize_model(model: str):

    if not model:
        return ""

    return (
        model.upper()
        .replace("-", "")
        .replace(" ", "")
    )


# ==========================================================
# Expand Keyword
# ==========================================================

def expand_keywords(question: str):

    q = question.lower()

    keywords = {question}

    mapping = {

        "steam": [
            "steam",
            "steam valve",
            "steam trap",
            "steam coil",
            "steam air vent",
            "solenoid",
            "valve",
            "coil",
            "trap",
        ],

        "สตีม": [
            "steam",
            "steam valve",
            "steam trap",
            "steam coil",
            "solenoid",
            "valve",
        ],

        "motor": [
            "motor",
            "drive",
        ],

        "มอเตอร์": [
            "motor",
        ],

        "bearing": [
            "bearing",
            "y-bearing",
        ],

        "ลูกปืน": [
            "bearing",
            "y-bearing",
        ],

    }

    for key, values in mapping.items():

        if key in q:

            keywords.update(values)

    return list(keywords)


# ==========================================================
# Remove Duplicate
# ==========================================================

def remove_duplicate(rows):

    unique = []
    seen = set()

    for row in rows:

        key = tuple(row)

        if key not in seen:

            seen.add(key)

            unique.append(row)

    return unique


# ==========================================================
# Parts
# ==========================================================

def search_parts(
    model="",
    question="",
):

    results = []

    model = normalize_model(model)

    for kw in expand_keywords(question):

        results.extend(

            repo_parts(

                keyword=kw,

                model=model,

            )

        )

    return remove_duplicate(results)


# ==========================================================
# Manuals
# ==========================================================

def search_manual(
    model="",
    question="",
):

    results = []

    model = normalize_model(model)

    for kw in expand_keywords(question):

        results.extend(

            repo_manuals(

                keyword=kw,

                model=model,

            )

        )

    return remove_duplicate(results)


# ==========================================================
# Repairs
# ==========================================================

def search_repair(
    model="",
    question="",
):

    results = []

    model = normalize_model(model)

    for kw in expand_keywords(question):

        results.extend(

            repo_repairs(

                keyword=kw,

                model=model,

            )

        )

    return remove_duplicate(results)