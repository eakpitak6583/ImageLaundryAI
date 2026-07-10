"""
LaundryBot V5

Prompt Engine
"""

from ai.prompt_builder import build_prompt


# ==========================================================
# Limit Knowledge
# ==========================================================

def compress_knowledge(knowledge: dict):

    return {

        "parts": knowledge.get("parts", [])[:10],

        "manual": knowledge.get("manual", [])[:5],

        "repair": knowledge.get("repair", [])[:10],

    }


# ==========================================================
# Prompt
# ==========================================================

def create_prompt(
    question: str,
    knowledge: dict,
):

    knowledge = compress_knowledge(
        knowledge,
    )

    return build_prompt(
        question=question,
        knowledge=knowledge,
    )