"""
LaundryBot V5

Prompt Builder
"""


# ==========================================================
# Text Truncate
# ==========================================================

def truncate(text, limit=600):

    if text is None:
        return ""

    text = str(text)

    if len(text) <= limit:
        return text

    return text[:limit] + " ..."


# ==========================================================
# Parts
# ==========================================================

def format_parts(parts):

    if not parts:
        return "ไม่พบข้อมูล"

    result = []

    for row in parts[:10]:

        result.append(f"""
Part Number : {row[1]}

Description : {row[2]}

Page : {row[3]}
""")

    return "\n".join(result)


# ==========================================================
# Manual
# ==========================================================

def format_manual(manuals):

    if not manuals:
        return "ไม่พบข้อมูล"

    result = []

    for row in manuals[:5]:

        result.append(f"""
Model : {row[0]}

Page : {row[1]}

Content

{truncate(row[2], 600)}
""")

    return "\n".join(result)


# ==========================================================
# Repair History
# ==========================================================

def format_repairs(repairs):

    if not repairs:
        return "ไม่พบข้อมูล"

    result = []

    for row in repairs[:10]:

        result.append(f"""
Complaint

{row[2] if len(row) > 2 else "-"}

Repair Action

{truncate(row[5] if len(row) > 5 else "-", 400)}

Result

{truncate(row[6] if len(row) > 6 else "-", 250)}
""")

    return "\n".join(result)


# ==========================================================
# Database Summary
# ==========================================================

def database_summary(knowledge):

    return f"""
Parts Found      : {len(knowledge.get("parts", []))}

Manual Pages     : {len(knowledge.get("manual", []))}

Repair History   : {len(knowledge.get("repair", []))}
"""


# ==========================================================
# Prompt Builder
# ==========================================================

def build_prompt(question, knowledge):

    return f"""
คุณคือ LaundryBot AI

คุณเป็นหัวหน้าช่าง Service เครื่องซักผ้าอุตสาหกรรม IMAGE

==========================
กฎการตอบ
==========================

1. ใช้ข้อมูลจากฐานข้อมูลเป็นหลัก

2. ห้ามสร้างข้อมูลที่ไม่มีอยู่จริง

3. ถ้าไม่มีข้อมูลให้แจ้งว่า

"ไม่พบข้อมูลในฐานข้อมูล"

4. สามารถใช้ความรู้ช่างทั่วไปเพิ่มเติมได้
แต่ต้องระบุว่าเป็น "ข้อเสนอแนะเพิ่มเติม"

==================================================
PARTS
==================================================

{format_parts(knowledge["parts"])}

==================================================
MANUAL
==================================================

{format_manual(knowledge["manual"])}

==================================================
REPAIR HISTORY
==================================================

{format_repairs(knowledge["repair"])}

==================================================
DATABASE SUMMARY
==================================================

{database_summary(knowledge)}

==================================================
QUESTION
==================================================

{question}

==================================================
รูปแบบคำตอบ
==================================================

1. วิเคราะห์สาเหตุที่เป็นไปได้
   (เรียงจากความเป็นไปได้มากที่สุด)

2. ขั้นตอนการตรวจสอบ

3. อะไหล่ที่เกี่ยวข้อง

- Part Number
- Description

4. อ้างอิงคู่มือ

- หน้า
- หัวข้อ

5. ประวัติการซ่อมที่คล้ายกัน

6. ข้อเสนอแนะเพิ่มเติม

7. ระดับความมั่นใจของคำตอบ
(High / Medium / Low)
"""