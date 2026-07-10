"""
LaundryBot V3

Backward Compatibility

AI Logic ถูกย้ายไปที่

knowledge_engine.pipeline
"""

from knowledge_engine.pipeline import answer_question


def ask_service_ai(
    model: str,
    question: str,
):

    return answer_question(
        model=model,
        question=question,
    )