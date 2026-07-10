from collections import Counter
from database.db import connect

# ================================
# Knowledge Dictionary
# ================================
KEYWORDS = {

    "Steam Valve": [
        "steam valve",
        "steam",
        "solenoid",
        "solinoid",
        "วาล์ว",
        "โซลินอยด์",
        "สตีม",
    ],

    "Steam Coil": [
        "steam coil",
        "coil",
        "คอยล์",
    ],

    "Bearing": [
        "bearing",
        "y-bearing",
        "ลูกปืน",
    ],

    "Motor": [
        "motor",
        "มอเตอร์",
    ],

    "Sensor": [
        "sensor",
        "rtd",
        "เซ็นเซอร์",
    ],

    "Inverter": [
        "inverter",
        "อินเวอร์เตอร์",
    ],

    "Belt": [
        "belt",
        "สายพาน",
    ],

    "Chain": [
        "chain",
        "โซ่",
    ],

    "Pump": [
        "pump",
        "ปั๊ม",
    ],

    "Cylinder": [
        "cylinder",
        "air cylinder",
        "กระบอกลม",
    ],

    "Door": [
        "door",
        "ประตู",
    ],

    "PLC": [
        "plc",
    ],

    "Sensor Cable": [
        "สาย sensor",
        "สายเซ็นเซอร์",
    ],

}


def top_failures(model, limit=10):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            complaint,
            detail,
            repair_action,
            result
        FROM repair_history
        WHERE machine_model=?
    """, (model,))

    rows = cursor.fetchall()

    conn.close()

    counter = Counter()

    for row in rows:

        text = " ".join([
            row[0] or "",
            row[1] or "",
            row[2] or "",
            row[3] or "",
        ]).lower()

        for group, words in KEYWORDS.items():

            if any(w.lower() in text for w in words):

                counter[group] += 1

    return counter.most_common(limit)
def top_problems(model, limit=10):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT complaint
    FROM repair_history
    WHERE machine_model=?
    """, (model,))

    rows = cursor.fetchall()

    conn.close()

    counter = Counter()

    for row in rows:

        if row[0]:

            counter[row[0].strip()] += 1

    return counter.most_common(limit)
def top_parts(model, limit=10):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        description
    FROM parts
    WHERE model=?
    """, (model,))

    rows = cursor.fetchall()

    conn.close()

    counter = Counter()

    for row in rows:

        if row[0]:

            counter[row[0]] += 1

    return counter.most_common(limit)