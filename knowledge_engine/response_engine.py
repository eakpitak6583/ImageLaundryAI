"""
LaundryBot V3

Response Engine
"""


def format_answer(answer: str):

    if not answer:

        return "ไม่พบข้อมูล"

    return answer.strip()