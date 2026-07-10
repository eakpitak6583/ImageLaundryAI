from flask import Blueprint
from flask import render_template
from flask import request

from flask_login import login_required

from services.ai_chat_service import ask_ai

ai_chat = Blueprint(
    "ai_chat",
    __name__,
)


@ai_chat.route("/ai-chat", methods=["GET", "POST"])
@login_required
def index():

    model = ""
    question = ""
    answer = ""
    error = ""

    if request.method == "POST":

        model = request.form.get("model", "").strip()
        question = request.form.get("question", "").strip()

        if not model:
            error = "กรุณาระบุ Model"

        elif not question:
            error = "กรุณาระบุคำถาม"

        else:
            try:
                answer = ask_ai(
                    model=model,
                    question=question,
                )
            except Exception as e:
                error = str(e)

    return render_template(
        "ai_chat.html",
        model=model,
        question=question,
        answer=answer,
        error=error,
    )