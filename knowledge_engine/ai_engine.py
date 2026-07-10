from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(
    BASE_DIR / ".env"
)

client = OpenAI()


def ask_gpt(
    prompt: str,
):

    response = client.responses.create(

        model="gpt-5.5",

        input=prompt,

    )

    return response.output_text