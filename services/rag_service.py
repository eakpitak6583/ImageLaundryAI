"""
LaundryBot V7 Enterprise
RAG Service
"""

from pathlib import Path

from openai import OpenAI
from langchain_community.vectorstores import FAISS

from config import Config
from services.embedding_service import embedding_service


class RagService:

    def __init__(self):

        self.client = OpenAI(
            api_key=Config.OPENAI_API_KEY
        )

        self.vector_db = None

    # ======================================================
    # Load Vector Database
    # ======================================================

    def load(self):

        if self.vector_db is not None:

            return self.vector_db

        index = Path(Config.VECTOR_DB) / "index.faiss"

        if not index.exists():

            return None

        self.vector_db = FAISS.load_local(

            Config.VECTOR_DB,

            embedding_service.embeddings,

            allow_dangerous_deserialization=True,

        )

        return self.vector_db

    # ======================================================
    # Search
    # ======================================================

    def search(

        self,

        question,

        top_k=5,

    ):

        db = self.load()

        if db is None:

            return ""

        docs = db.similarity_search(

            question,

            k=top_k,

        )

        text = []

        for doc in docs:

            filename = doc.metadata.get(

                "filename",

                "",

            )

            page = doc.metadata.get(

                "page",

                "",

            )

            text.append(

                f"""
FILE : {filename}
PAGE : {page}

{doc.page_content}
"""
            )

        return "\n\n".join(text)

    # ======================================================
    # Ask AI
    # ======================================================

    def ask(

        self,

        question,

        top_k=5,

    ):

        knowledge = self.search(

            question,

            top_k,

        )

        prompt = f"""
คุณคือ LaundryBot V7 Enterprise

ใช้ข้อมูลจาก Manual และ Repair History เท่านั้น

==========================
Knowledge
==========================

{knowledge}

==========================
Question
==========================

{question}

หากไม่มีข้อมูลให้ตอบว่า

"ไม่พบข้อมูลในฐานความรู้"

ห้ามเดา
"""

        response = self.client.responses.create(

            model=Config.MODEL_NAME,

            input=prompt,

        )

        return response.output_text.strip()

    # ======================================================
    # Ask with Repair Context
    # ======================================================

    def ask_machine(

        self,

        machine,

        symptom,

    ):

        query = f"""

Machine

{machine}

Problem

{symptom}

"""

        return self.ask(query)

    # ======================================================
    # Ask Manual
    # ======================================================

    def ask_manual(

        self,

        machine,

        keyword,

    ):

        return self.ask(

            f"{machine}\n{keyword}"

        )


rag_service = RagService()