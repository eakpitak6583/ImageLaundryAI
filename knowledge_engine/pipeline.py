"""
LaundryBot V5

Knowledge Pipeline

Flow

Question
    ↓
Intent
    ↓
Search
    ↓
Ranking
    ↓
Prompt
    ↓
GPT
    ↓
Response
"""

from knowledge_engine.intent_engine import detect_intent
from knowledge_engine.search_engine import search_knowledge
from knowledge_engine.ranking_engine import rank_knowledge
from knowledge_engine.prompt_engine import create_prompt
from knowledge_engine.ai_engine import ask_gpt
from knowledge_engine.response_engine import format_answer


# ==========================================================
# Main Pipeline
# ==========================================================

def answer_question(
    model: str,
    question: str,
):

    # ---------------------------------------
    # Intent
    # ---------------------------------------

    intent = detect_intent(question)

    keyword = intent["keyword"]

    # ---------------------------------------
    # Search
    # ---------------------------------------

    knowledge = search_knowledge(

        model=model,

        keyword=keyword,

    )

    # ---------------------------------------
    # Ranking
    # ---------------------------------------

    knowledge = rank_knowledge(

        knowledge=knowledge,

        keyword=keyword,

    )

    # ---------------------------------------
    # Prompt
    # ---------------------------------------

    prompt = create_prompt(

        question=question,

        knowledge=knowledge,

    )

    # ---------------------------------------
    # GPT
    # ---------------------------------------

    answer = ask_gpt(

        prompt=prompt,

    )

    # ---------------------------------------
    # Response
    # ---------------------------------------

    return format_answer(

        answer,

    )