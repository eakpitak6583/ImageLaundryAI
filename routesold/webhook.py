from pathlib import Path
import os

from dotenv import load_dotenv

from flask import Blueprint, request

from linebot.v3.webhook import WebhookHandler
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from services.line_service import reply_text
from ai.service_ai import ask_service_ai

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

handler = WebhookHandler(
    os.getenv("LINE_CHANNEL_SECRET")
)

webhook = Blueprint("webhook", __name__)


@webhook.route("/webhook", methods=["POST"])
def callback():

    signature = request.headers.get("X-Line-Signature")

    body = request.get_data(as_text=True)

    handler.handle(body, signature)

    return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):

    question = event.message.text.strip()

    model = "DI225"

    if question.upper().startswith("DP250"):
        model = "DP250"

    elif question.upper().startswith("DI475"):
        model = "DI475"

    elif question.upper().startswith("X-DRYER120"):
        model = "X-DRYER120"

    answer = ask_service_ai(model, question)

    reply_text(
        event.reply_token,
        answer,
    )