"""
LaundryBot V5

Ranking Engine
"""

from difflib import SequenceMatcher


# ==========================================================
# Similarity
# ==========================================================

def similarity(a: str, b: str):

    if not a or not b:
        return 0

    return SequenceMatcher(
        None,
        a.lower(),
        b.lower(),
    ).ratio()


# ==========================================================
# Record Score
# ==========================================================

def record_score(
    record,
    keyword,
):

    score = 0

    text = " ".join(
        map(str, record)
    ).lower()

    keyword = keyword.lower()

    # ----------------------------------
    # Exact Match
    # ----------------------------------

    if keyword in text:

        score += 100

    # ----------------------------------
    # Similarity
    # ----------------------------------

    score += similarity(
        keyword,
        text,
    ) * 50

    # ----------------------------------
    # Machine Model Priority
    # ----------------------------------

    if len(record) > 0:

        model = str(record[0]).lower()

        if keyword == model:

            score += 200

    # ----------------------------------
    # Part Number Priority
    # ----------------------------------

    for item in record:

        value = str(item).lower()

        if value == keyword:

            score += 150

    return score


# ==========================================================
# Rank List
# ==========================================================

def rank_records(
    records,
    keyword,
):

    ranked = []

    for row in records:

        ranked.append(

            (

                record_score(

                    row,

                    keyword,

                ),

                row,

            )

        )

    ranked.sort(

        reverse=True,

        key=lambda x: x[0],

    )

    return [

        r[1]

        for r in ranked

    ]


# ==========================================================
# Knowledge
# ==========================================================

def rank_knowledge(

    knowledge,

    keyword,

):

    result = {}

    for table, rows in knowledge.items():

        result[table] = rank_records(

            rows,

            keyword,

        )

    return result