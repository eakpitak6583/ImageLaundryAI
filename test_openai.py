from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

print("KEY =", os.getenv("OPENAI_API_KEY"))

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    result = client.embeddings.create(
        model="text-embedding-3-small",
        input="Hello"
    )

    print("SUCCESS")
    print(result.data[0].embedding[:5])

except Exception as e:
    print(e)