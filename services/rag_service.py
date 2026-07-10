"""
LaundryBot V7 Enterprise
Enterprise RAG Service
"""

from openai import OpenAI

from config import Config
from services.embedding_service import embedding_service


class RAGService:

    def __init__(self):

        self.client = OpenAI(
            api_key=Config.OPENAI_API_KEY
        )

    # ======================================================
    # Build Context
    # ======================================================

    def _build_context(self, docs):

        context = []

        sources = []

        seen = set()

        for doc in docs:

            filename = doc.metadata.get(
                "filename",
                "Unknown"
            )

            page = int(
                doc.metadata.get(
                    "page",
                    0
                )
            )

            score = float(
                doc.metadata.get(
                    "score",
                    1.0
                )
            )

            key = (filename, page)

            if key not in seen:

                seen.add(key)

                sources.append({

                    "filename": filename,

                    "page": page,

                    "score": round(score, 4),

                })

            context.append(
                f"""
==================================================

DOCUMENT : {filename}

PAGE : {page}

==================================================

{doc.page_content}

"""
            )

        return "\n".join(context), sources

    # ======================================================
    # Build Search Keyword
    # ======================================================

    def _build_search_keyword(self, question):

        keyword = question

        remove_words = [

            "อยู่หน้าไหน",
            "อยู่หน้า",
            "หน้าไหน",
            "คืออะไร",
            "คือ",
            "ทำงานอย่างไร",
            "ทำงานยังไง",
            "วิธี",
            "อย่างไร",
            "ยังไง",
            "มีไหม",
            "อธิบาย",
            "?",
            "？",

        ]

        for word in remove_words:

            keyword = keyword.replace(
                word,
                ""
            )

        return keyword.strip()

    # ======================================================
    # Ask
    # ======================================================

    def ask(self, question):

        question = question.strip()

        if question == "":

            return {

                "answer": "กรุณาพิมพ์คำถาม",

                "sources": [],

                "search_keyword": "",

                "confidence": 0,

                "document_count": 0,

            }

        docs = embedding_service.similarity_search(

            question,

            k=5,

        )

        if not docs:

            return {

                "answer": "ไม่พบข้อมูลในคู่มือ",

                "sources": [],

                "search_keyword": self._build_search_keyword(question),

                "confidence": 0,

                "document_count": 0,

            }

        context, sources = self._build_context(docs)

        prompt = f"""
คุณคือ LaundryBot AI Enterprise

คุณเป็นผู้ช่วยช่างซ่อมเครื่องซักผ้าอุตสาหกรรม

กฎในการตอบ

1. ตอบจาก CONTEXT เท่านั้น

2. ห้ามเดา

3. ถ้าไม่มีข้อมูลให้ตอบว่า

ไม่พบข้อมูลในคู่มือ

4. ตอบเป็นภาษาไทย

5. จัดรูปแบบให้อ่านง่าย

6. หากมีหลายรายการให้เรียงเป็นข้อ

7. หากพบ Part Number ให้แสดง

8. หากพบ Specification ให้แสดง

9. ห้ามสร้างข้อมูลเพิ่ม

10. อ้างอิงชื่อเอกสารและเลขหน้าที่ใช้จริง

============================
CONTEXT
============================

{context}

============================
QUESTION
============================

{question}
"""

        response = self.client.responses.create(

            model=Config.MODEL_NAME,

            input=prompt,

        )

        confidence = 0

        if sources:

            scores = [

                item["score"]

                for item in sources

            ]

            confidence = round(

                sum(scores) / len(scores),

                4

            )

        return {

            "answer": response.output_text.strip(),

            "sources": sources,

            "search_keyword": self._build_search_keyword(question),

            "confidence": confidence,

            "document_count": len(sources),

        }

    # ======================================================
    # Search
    # ======================================================

    def search(self, question):

        return embedding_service.similarity_search(

            question,

            k=10,

        )


rag_service = RAGService()