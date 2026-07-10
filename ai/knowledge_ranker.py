from collections import Counter
import re


def tokenize(text: str):

    if not text:
        return []

    return re.findall(r"[A-Za-z0-9ก-๙]+", text.lower())


def score(question, text, weight):

    q = Counter(tokenize(question))
    t = Counter(tokenize(text))

    score = 0

    for word in q:

        if word in t:
            score += q[word] * t[word] * weight

    return score


def rank_knowledge(knowledge, question):

    # --------------------
    # PARTS
    # --------------------

    part_scores = []

    for row in knowledge["parts"]:

        text = " ".join(str(x) for x in row)

        s = score(question, text, 2)

        part_scores.append((s, row))

    part_scores.sort(reverse=True, key=lambda x: x[0])

    # --------------------
    # MANUAL
    # --------------------

    manual_scores = []

    for row in knowledge["manual"]:

        text = " ".join(str(x) for x in row)

        s = score(question, text, 3)

        manual_scores.append((s, row))

    manual_scores.sort(reverse=True, key=lambda x: x[0])

    # --------------------
    # REPAIR
    # --------------------

    repair_scores = []

    for row in knowledge["repair"]:

        complaint = str(row[0])
        detail = str(row[1])
        repair = str(row[2])
        result = str(row[3])

        s = 0

        s += score(question, complaint, 10)
        s += score(question, detail, 7)
        s += score(question, repair, 6)
        s += score(question, result, 3)

        repair_scores.append((s, row))

    repair_scores.sort(reverse=True, key=lambda x: x[0])

    return {
        "parts": [x[1] for x in part_scores[:5]],
        "manual": [x[1] for x in manual_scores[:3]],
        "repair": [x[1] for x in repair_scores[:5]],
    }