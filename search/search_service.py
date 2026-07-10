"""
LaundryBot V3

AI Chat Service

หน้าที่ :
- รับคำถามจาก Route
- ส่งต่อเข้า Knowledge Pipeline
"""

from knowledge_engine.pipeline import answer_question


def ask_ai(
    model: str,
    question: str,
):

    return answer_question(
        model=model,
        question=question,
    )