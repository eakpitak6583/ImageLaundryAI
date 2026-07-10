from flask import (
    Blueprint,
    request,
    jsonify,
)

from services.ai_analysis_service import create_ai_input
from knowledge_engine.analysis_engine import analyze_service

ai_analysis = Blueprint(
    "ai_analysis",
    __name__,
)


@ai_analysis.route(
    "/api/ai-analysis",
    methods=["POST"],
)
def ai_analysis_api():

    data = request.json

    model = data.get("model", "")

    keyword = data.get("keyword", "")

    ai_data = create_ai_input(

        model,

        keyword,

    )

    answer = analyze_service(

        model,

        keyword,

        ai_data["context"],

    )

    return jsonify({

        "answer": answer,

        "statistics": ai_data["statistics"],

    })