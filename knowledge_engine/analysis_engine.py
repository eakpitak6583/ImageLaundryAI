"""
LaundryBot V4

Analysis Engine
"""

from knowledge_engine.prompt_engine import create_prompt
from knowledge_engine.ai_engine import ask_gpt


def analyze_service(
    model,
    keyword,
    knowledge,
):

    prompt = create_prompt(

        question=keyword,

        knowledge=knowledge,

    )

    answer = ask_gpt(

        prompt,

    )

    return answer